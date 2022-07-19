import base64
from pathlib import Path
from typing import Any

import requests
from celery import shared_task

from .predict import load_model, predict
from .preprocessing import pre_process

MODELS: dict[str, Any] = {}


@shared_task
def get_prediction(image_path: str) -> dict:

    preprocessed_image = pre_process(base64.decodebytes(image_path.encode("ascii")))
    model_path = Path(__file__).parent / "cv_models" / "image-content-filtration.h5"
    if model_path not in MODELS:
        MODELS[str(model_path)] = load_model(model_path)

    model = MODELS[str(model_path)]
    return predict(model, preprocessed_image)


@shared_task
def get_prediction_from_url(image_url: str) -> dict:

    # maybe move this to the worker instead
    response = requests.get(
        image_url,
        headers={
            "User-Agent": "predict.ml-collab-2022/0.1 (http://predict-ml-collab-2022.wikimedia.org dcaro@wikimedia.org) python-requests"
        },
        stream=True,
    )
    response.raise_for_status()

    preprocessed_image = pre_process(response.raw.read())
    model_path = Path(__file__).parent / "cv_models" / "image-content-filtration.h5"
    if model_path not in MODELS:
        MODELS[str(model_path)] = load_model(model_path)

    model = MODELS[str(model_path)]
    return predict(model, preprocessed_image)


# @shared_task
# def divide(x, y):
#     import time

#     time.sleep(5)

#     return x / 5
