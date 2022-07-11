import eventlet  #  enable WebSocket support
eventlet.monkey_patch()


from cv_model_serve import create_app, socketio

app = create_app()


@app.route("/")
def hello():
    return "Hello, World!"


if __name__ == '__main__':
    socketio.run(
        app,
        debug=True,
        use_reloader=True,
        host='0.0.0.0'
    )