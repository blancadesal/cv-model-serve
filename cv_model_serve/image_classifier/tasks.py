import base64
from pathlib import Path

from celery import shared_task

from .predict import load_model, predict
from .preprocessing import pre_process


@shared_task
def get_prediction(image_path: str) -> dict:

    preprocessed_image = pre_process(base64.decodebytes(image_path.encode("ascii")))
    model = load_model(
        Path(__file__).parent / "cv_models" / "image-content-filtration.h5"
    )
    return predict(model, preprocessed_image)


# @shared_task
# def divide(x, y):
#     import time

#     time.sleep(5)

#     return x / 5
