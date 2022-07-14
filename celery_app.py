import subprocess
from cv_model_serve import create_app, ext_celery

from cv_model_serve.image_classifier import (
    tasks,
)  # noqa, needed to load the shared tasks


app = create_app()
celery = ext_celery.celery


def run_worker():
    subprocess.call(["celery", "-A", "celery_app.celery", "worker", "--loglevel=info"])


@app.cli.command("celery_worker")
def celery_worker():
    from watchgod import run_process

    run_process("./cv_model_serve", run_worker)
