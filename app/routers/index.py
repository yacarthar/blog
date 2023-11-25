from flask import make_response, render_template
from flask_restx import Namespace, Resource

from app.services.post import list_post

api = Namespace("index")


@api.route("home")
class Home(Resource):
    @classmethod
    def get(cls):
        posts = list_post()
        return make_response(render_template("home.html", posts=posts))
