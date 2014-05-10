from flask import Flask
from werkzeug.utils import import_string


blueprints = [
    'ailtdou.main.views.bp',
    'ailtdou.user.views.bp',
]


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('app.cfg')
    app.config.from_envvar('AILTDOU_CONFIG', silent=True)

    register_blueprints(app, blueprints)

    return app


def register_blueprints(app, import_names):
    blueprints = [import_string(n) for n in import_names]
    for bp in blueprints:
        app.register_blueprint(bp)
    return blueprints
