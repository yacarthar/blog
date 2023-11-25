from flask import request, make_response, render_template
from flask_restx import Namespace, Resource

from app.services.post import create_post, get_post, list_post

api = Namespace("post")


@api.route("/")
class Posts(Resource):
    @classmethod
    def get(cls):
        raw_posts = list_post()
        posts = [p.to_json() for p in raw_posts]
        return make_response(render_template("posts.html", posts=posts))

    @classmethod
    def post(cls):
        data = request.json
        new_post = create_post(data)
        return new_post.to_json()


@api.route("/<path>")
class Post(Resource):
    @classmethod
    def get(cls, path):
        *words, post_id = path.split("-")
        raw_post = get_post(post_id)
        assert request.path == raw_post.link
        post = raw_post.to_json()
        return make_response(render_template("post.html", post=post))
