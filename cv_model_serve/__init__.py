import os
from pathlib import Path

from flask import Flask
from flask_celeryext import FlaskCeleryExt

from cv_model_serve.celery_utils import make_celery
from cv_model_serve.config import config

# instantiate extensions
ext_celery = FlaskCeleryExt(create_celery_app=make_celery)


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
