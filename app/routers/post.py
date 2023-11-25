from flask import request, make_response, render_template
from flask_restx import Namespace, Resource

from app.services.post import create_post, get_post, list_post
from app.libs.helper import generate_link

api = Namespace("post")


@api.route("/")
class Posts(Resource):
    @classmethod
    def get(cls):
        posts = list_post()
        return make_response(render_template("posts.html", posts=posts))

    @classmethod
    def post(cls):
        data = request.json
        new_post = create_post(data)
        return new_post


@api.route("/<path>")
class Post(Resource):
    @classmethod
    def get(cls, path):
        *words, post_id = path.split("-")
        post = get_post(post_id)
        assert request.path == generate_link(post["title"], post["id"])
        return post
