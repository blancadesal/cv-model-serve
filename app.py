import base64
import subprocess

from flask import request

from cv_model_serve import create_app, ext_celery
from cv_model_serve.image_classifier.tasks import get_prediction

app = create_app()
celery = ext_celery.celery


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/predict", methods=["POST"])
def predict():
    image = request.files["image"].read()

    task = get_prediction.delay(base64.encodebytes(image).decode("ascii"))
    return task.id


def run_worker():
    subprocess.call(["celery", "-A", "app.celery", "worker", "--loglevel=info"])


@app.cli.command("celery_worker")
def celery_worker():
    from watchgod import run_process

    run_process("./cv_model_serve", run_worker)
