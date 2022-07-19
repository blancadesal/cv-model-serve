import subprocess

from flasgger import Swagger
from flask_restful import Api

from api import create_app, ext_celery
from api.resources.index import Index, Username
from api.resources.predict import Predict, Results

app = create_app()
api = Api(app)
celery = ext_celery.celery
swagger = Swagger(app)


# Routes
api.add_resource(Index, "/")
api.add_resource(Predict, "/predict")
api.add_resource(Results, "/results/<task_id>")
api.add_resource(Username, "/username/<username>")  # Just to test Swagger


# Enable celery auto reloading
def run_worker():
    subprocess.call(["celery", "-A", "app.celery", "worker", "--loglevel=info"])


@app.cli.command("celery_worker")
def celery_worker():
    from watchgod import run_process

    run_process("./api", run_worker)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="0.0.0.0")
