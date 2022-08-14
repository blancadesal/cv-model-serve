import base64
from typing import Any

import requests
from celery import shared_task

from . import models
from .models import get_model
from .predict import predict
from .preprocessing import pre_process


@shared_task
def get_prediction(
    image_path: str, model_name: str = models.DEFAULT_MODEL
) -> dict[str, Any]:

    preprocessed_image = pre_process(base64.decodebytes(image_path.encode("ascii")))
    model = get_model(model_name)
    return predict(model, preprocessed_image)


@shared_task
def get_prediction_from_url(
    image_url: str, model_name: str = models.DEFAULT_MODEL
) -> dict[str, Any]:

    # maybe move this to the worker instead
    response = requests.get(
        image_url,
        headers={
            "User-Agent": "predict.commtech/0.1 (http://image_predict.commtech.wmcloud.org dcaro@wikimedia.org) python-requests"
        },
        stream=True,
    )
    response.raise_for_status()

    preprocessed_image = pre_process(response.raw.read())
    model = get_model(model_name)
    return predict(model, preprocessed_image)
