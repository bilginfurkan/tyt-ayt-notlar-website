from flask import Flask, g
from flask_misaka import Misaka
from flask_caching import Cache
import os


md = Misaka()
cache = Cache(config={"CACHE_TYPE": "null"})


def register_extensions(app):
    md.init_app(app)
    cache.init_app(app)


def register_config(app):    
    pass


def create_app():
    app = Flask(__name__)
    with app.app_context():
        register_config(app)
        register_extensions(app)

        import routes

    return app