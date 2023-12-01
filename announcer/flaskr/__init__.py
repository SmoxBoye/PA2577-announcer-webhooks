import os
import json

from flask import Flask


def create_app(test_config=None):
    """create_app Factory function to create and configure the Flask app

    Args:
        test_config (dict, optional): Alternative configuration for testing. Defaults to None.

    Returns:
        Flask: configured Flask app
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # app.config.from_mapping(
    #     SECRET_KEY="f339b45b-69cf-4d24-8205-1a1f57b5aeb7",

    # )

    app.config.from_prefixed_env()

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # app.config.from_pyfile('config.py', silent=True)
        app.config.from_prefixed_env()
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # Init database
    # from . import db

    # db.init_app(app)

    # Register core functionality blueprint
    from . import core

    app.register_blueprint(core.bp)

    return app
