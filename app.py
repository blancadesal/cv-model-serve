import base64
import subprocess

from celery.result import AsyncResult
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
    task: AsyncResult = get_prediction.delay(base64.encodebytes(image).decode("ascii"))
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

