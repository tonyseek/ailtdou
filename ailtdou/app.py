from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('app.cfg')
    app.config.from_envvar('AILTDOU_CONFIG', silent=True)

    return app
