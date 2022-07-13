import base64
import eventlet  #  enable WebSocket support
eventlet.monkey_patch()

import flask
from cv_model_serve.image_classifier.tasks import get_prediction



from cv_model_serve import create_app, socketio

app = create_app()


@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/predict", methods=["POST"])
def predict():
    image = flask.request.files["image"].read()

    task = get_prediction.delay(base64.encodebytes(image).decode('ascii'))
    return task.id



if __name__ == '__main__':
    socketio.run(
        app,
        debug=True,
        use_reloader=True,
        host='0.0.0.0'
    )