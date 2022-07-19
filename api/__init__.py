import os

from celery import current_app as current_celery_app
from flask import Flask
from flask_celeryext import FlaskCeleryExt

from api.config import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "development")

    # instantiate the app
    app = Flask(__name__)

    # set config
    app.config.from_object(config[config_name])

    # set up extensions
    ext_celery.init_app(app)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app}

    return app


def make_celery(app):
    celery = current_celery_app
    celery.config_from_object(app.config, namespace="CELERY")

    return celery


ext_celery = FlaskCeleryExt(create_celery_app=make_celery)
