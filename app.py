import base64
import subprocess

from celery.result import AsyncResult
from flask import request

from cv_model_serve import create_app, ext_celery
from cv_model_serve.image_classifier.tasks import (
    get_prediction,
    get_prediction_from_url,
)

app = create_app()
celery = ext_celery.celery


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/predict", methods=["POST"])
def predict_form_post():
    image = request.files["image"].read()
    model_name = request.args.get("model_name", None)
    params = {"image_url": base64.encodebytes(image).decode("ascii")}
    if model_name:
        params["model_name"] = model_name

    task: AsyncResult = get_prediction.delay(**params)
    return {"task_id": task.id}


@app.route("/predict", methods=["GET"])
def predict_from_url():
    image_url = request.args.get("image_url", None)
    model_name = request.args.get("model_name", None)
    if image_url is None:
        return "Parameter image_url not found.", 400
    if not image_url.startswith("https://upload.wikimedia.org"):
        return "Only urls from https://upload.wikimedia.org are allowed", 400

    params = {"image_url": image_url}
    if model_name:
        params["model_name"] = model_name
    task: AsyncResult = get_prediction_from_url.delay(**params)
    return {"task_id": task.id}


@app.route("/task/<task_id>", methods=["GET"])
def get_task(task_id: str):
    my_task = AsyncResult(task_id)
    response = {
        "task_id": task_id,
        "state": my_task.state,
    }
    if my_task.state == "FAILURE":
        response.update(
            {
                "error": str(my_task.result),
                "result": None,
            }
        )
    else:
        response.update(
            {
                "error": None,
                "result": (
                    my_task.result if my_task.result is None else str(my_task.result)
                ),
            }
        )
    return response


def run_worker():
    subprocess.call(["celery", "-A", "app.celery", "worker", "--loglevel=info"])


@app.cli.command("celery_worker")
def celery_worker():
    from watchgod import run_process

    run_process("./cv_model_serve", run_worker)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="0.0.0.0")
