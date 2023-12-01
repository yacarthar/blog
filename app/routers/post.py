from flask import make_response, render_template, request
from flask_restx import Namespace, Resource
from pydantic import ValidationError
from werkzeug.utils import secure_filename

from app.libs.helper import allowed_file
from app.libs.log import logger
from app.libs.markdown import convert_to_html, extract_tag_body, generate_toc
from app.schemas.post import PostCreate, PostUpdate
from app.services.category import create_category
from app.services.post import (
    create_post,
    find_post_by_category,
    find_post_by_tag,
    get_post,
    list_post,
)
from app.services.tag import create_tag

api = Namespace("post")


@api.route("/")
class PostsHandler(Resource):
    @classmethod
    def get(cls):
        page_num = int(request.args.get("page", 1))
        page = list_post(page=page_num)
        posts = [p.to_json() for p in page.items]
        return make_response(
            render_template("posts.html", posts=posts, pagination=page)
        )


@api.route("/tag/<tag_name>")
class TagsHandler(Resource):
    @classmethod
    def get(cls, tag_name):
        page_num = int(request.args.get("page", 1))
        page = find_post_by_tag(tag_name, page_num)
        posts = [p.to_json() for p in page.items]
        return make_response(
            render_template("posts.html", posts=posts, pagination=page)
        )


@api.route("/category/<cat_name>")
class CatsHandler(Resource):
    @classmethod
    def get(cls, cat_name):
        page_num = int(request.args.get("page", 1))
        page = find_post_by_category(cat_name, page_num)
        posts = [p.to_json() for p in page.items]
        return make_response(
            render_template("posts.html", posts=posts, pagination=page)
        )


@api.route("/<path>")
class PostHandler(Resource):
    @classmethod
    def get(cls, path):
        *words, post_id = path.split("-")
        raw_post = get_post(post_id)
        if not raw_post or request.path != raw_post.link:
            return {"message": "not found"}, 404
        post = raw_post.to_json()
        return make_response(render_template("post.html", post=post))


@api.route("/api/<post_id>")
class PostApi(Resource):
    @classmethod
    def get(cls, post_id):
        post = get_post(post_id)
        if not post:
            return {"message": "not found"}, 404

        return post.to_json(short=100), 200

    @classmethod
    def put(cls, post_id):
        post = get_post(post_id)
        if not post:
            return {"message": "not found"}, 404

        file = request.files.get("file")
        if (
            file
            and file.filename != ""
            and allowed_file(secure_filename(file.filename))
        ):
            markdown_content = file.read().decode("utf-8")
            html_content = convert_to_html(markdown_content)
            post.content = extract_tag_body(html_content)
            post.toc = generate_toc(html_content)

        try:
            raw_data = request.form.to_dict()
            data = PostUpdate.model_validate(raw_data)
            data_dict = data.model_dump(exclude_none=True)
            for k, v in data_dict.items():
                setattr(post, k, v)
        except ValidationError as e:
            logger.error(e.json())
            return {"message": "Bad Request"}, 400

        tags = request.form.getlist("tag")
        if tags:
            for name in tags:
                tag = create_tag(name)
                post.tags.append(tag)
        post.save()
        post.refresh()

        cat_name = request.form.get("category")
        if cat_name:
            category = create_category(cat_name)
            post.category_id = category.id
            post.save()
            post.refresh()

        return post.to_json(short=100), 200


@api.route("/api/")
class PostsApi(Resource):
    @classmethod
    def get(cls):
        raw_page = list_post()
        posts = [p.to_json(short=50) for p in raw_page.items]
        return posts

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

        markdown_content = file.read().decode("utf-8")
        html_content = convert_to_html(markdown_content)

        post_content = extract_tag_body(html_content)
        toc = generate_toc(html_content)

        new_post = create_post(
            content=post_content, toc=toc, **data.model_dump()
        )

        tags = request.form.getlist("tag")
        if tags:
            for name in tags:
                tag = create_tag(name)
                new_post.tags.append(tag)
        new_post.save()
        new_post.refresh()

        cat_name = request.form.get("category")
        if cat_name:
            category = create_category(cat_name)
            new_post.category_id = category.id
            new_post.save()
            new_post.refresh()

        return new_post.to_json(short=100), 200
