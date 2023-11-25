from flask import Flask, redirect
from flask_restx import Api

from app.models import db
from app.routers.index import api as index_ns
from app.routers.post import api as post_ns
from configs import config


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    register_db(app)
    custom_route(app)
    register_api(app)
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
