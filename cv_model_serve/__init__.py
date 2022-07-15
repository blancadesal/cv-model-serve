import os

from flask import Flask
from flask_celeryext import FlaskCeleryExt
from flask_socketio import SocketIO

from cv_model_serve.celery_utils import make_celery
from cv_model_serve.config import config


from pathlib import Path


# instantiate extensions
ext_celery = FlaskCeleryExt(create_celery_app=make_celery)
socketio = SocketIO()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "development")

    # instantiate the app
    app = Flask(__name__)

    # set config
    app.config.from_object(config[config_name])

    # set up extensions
    ext_celery.init_app(app)
    socketio.init_app(app, message_queue=app.config["SOCKETIO_MESSAGE_QUEUE"])

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app}

    return app
