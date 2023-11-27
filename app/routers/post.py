from bs4 import BeautifulSoup
from flask import make_response, render_template, request
from flask_restx import Namespace, Resource
from pydantic import ValidationError
from werkzeug.utils import secure_filename

from app.libs.helper import allowed_file
from app.libs.log import logger
from app.schemas.post import PostCreate
from app.services.post import create_post, get_post, list_post
from app.services.tag import create_tag, get_tag_by_name

api = Namespace("post")


@api.route("/")
class PostsHandler(Resource):
    @classmethod
    def get(cls):
        raw_posts = list_post()
        posts = [p.to_json() for p in raw_posts]
        return make_response(render_template("posts.html", posts=posts))

    @classmethod
    def post(cls):
        if "file" not in request.files:
            return {"message": "file missing"}, 400
        file = request.files.get("file")
        if file.filename == "":
            return {"message": "file missing"}, 400
        if not allowed_file(secure_filename(file.filename)):
            return {"message": "invalid file type"}, 400

        try:
            raw_data = request.form.to_dict()
            data = PostCreate.model_validate(raw_data)
        except ValidationError as e:
            logger.error(e.json())
            return {"message": "Bad Request"}, 400

        soup = BeautifulSoup(file.read(), "html.parser")
        body_content = soup.body
        new_post = create_post(content=str(body_content), **data.model_dump())

        tags = request.form.getlist("tag")
        if tags:
            for name in tags:
                tag = create_tag(name)
                new_post.tags.append(tag)
        new_post.save()
        new_post.refresh()

        return new_post.to_json(short=100), 200


@api.route("/tags/<tag_name>")
class TagsHandler(Resource):
    @classmethod
    def get(cls, tag_name):
        tag = get_tag_by_name(tag_name)
        posts = [p.to_json() for p in tag.posts]
        return make_response(render_template("posts.html", posts=posts))


@api.route("/<path>")
class PostHandler(Resource):
    @classmethod
    def get(cls, path):
        *words, post_id = path.split("-")
        raw_post = get_post(post_id)
        assert request.path == raw_post.link
        post = raw_post.to_json()
        return make_response(render_template("post.html", post=post))
