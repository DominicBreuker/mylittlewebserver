from flask import Flask
from flask import Response


flask_app = Flask('flaskapp')


@flask_app.route('/')
def hello_world():
    return Response('Hi from Flask!\n', mimetype='text/plain')

app = flask_app.wsgi_app
