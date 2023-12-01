from flask import make_response, render_template
from flask_restx import Namespace, Resource

from app.services.post import list_post

api = Namespace("index")


@api.route("home")
class Home(Resource):
    @classmethod
    def get(cls):
        page = list_post()
        posts = [p.to_json() for p in page.items]
        return make_response(render_template("home.html", posts=posts))
