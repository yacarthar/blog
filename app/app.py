from flask import Flask, g, redirect, request
from flask_restx import Api

from app.libs.helper import build_url
from app.models import db
from app.routers.index import api as index_ns
from app.routers.post import api as post_ns
from app.services.category import get_top_categories
from app.services.tag import get_top_tags
from configs import config


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    register_db(app)
    custom_route(app)
    register_api(app)
    register_request_decorator(app)
    # print(app.config)
    return app


def register_db(app):
    db.init_app(app)


def custom_route(app):
    def get_home():
        return redirect("/home")

    app.add_url_rule("/", view_func=get_home)


def register_api(app):
    api = Api()
    api.init_app(app, add_specs=False)
    api.add_namespace(index_ns, "/")
    api.add_namespace(post_ns, "/posts")


def register_request_decorator(app):
    @app.before_request
    def load_top_categories():
        if request.endpoint is not None and "handler" in request.endpoint:
            g.top_categories = get_top_categories()
            g.top_tags = get_top_tags()
            g.build_url = build_url
