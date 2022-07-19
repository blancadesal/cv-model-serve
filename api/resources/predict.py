import base64

from celery.result import AsyncResult
from flask import request
from flask_restful import Resource

from api.prediction.tasks import get_prediction, get_prediction_from_url


class Predict(Resource):
    def get(self):
        """Predict from URL"""
        image_url = request.args.get("image_url", None)
        if image_url is None:
            return "Parameter image_url not found.", 400
        if not image_url.startswith("https://upload.wikimedia.org"):
            return "Only urls from https://upload.wikimedia.org are allowed", 400

        task: AsyncResult = get_prediction_from_url.delay(image_url)
        return {"task_id": task.id}

    def post(self):
        """Predict from image file"""
        image = request.files["image"].read()
        task: AsyncResult = get_prediction.delay(
            base64.encodebytes(image).decode("ascii")
        )
        return {"task_id": task.id}


class Results(Resource):
    def get(self, task_id):
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
                        my_task.result
                        if my_task.result is None
                        else str(my_task.result)
                    ),
                }
            )
        return response
