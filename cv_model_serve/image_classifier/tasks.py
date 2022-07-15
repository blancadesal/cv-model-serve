import base64
from pathlib import Path
from typing import Any

import requests
from celery import shared_task

from .predict import load_model, predict
from .preprocessing import pre_process

MODELS: dict[str, Any] = {}

DEFAULT_MODEL = "image-content-filtration.h5"
MODELS_DIR = Path(__file__).parent / "cv_models"


@shared_task
def get_prediction(image_path: str, model_name: str = DEFAULT_MODEL) -> dict[str, Any]:

    preprocessed_image = pre_process(base64.decodebytes(image_path.encode("ascii")))
    model = get_model(MODELS_DIR / model_name)
    return predict(model, preprocessed_image)


@shared_task
def get_prediction_from_url(
    image_url: str, model_name: str = DEFAULT_MODEL
) -> dict[str, Any]:

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
    model = get_model(MODELS_DIR / model_name)
    return predict(model, preprocessed_image)

