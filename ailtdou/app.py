from flask import Flask
from werkzeug.utils import import_string

from .ext import db, migrate, login_manager, oauth, sentry


blueprints = [
    'ailtdou.main.views.bp',
    'ailtdou.user.views.bp',
]


def create_app():
    app = Flask(__name__)
    app.config.from_object('envcfg.json.ailtdou')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    oauth.init_app(app)
    sentry.init_app(app)

    register_blueprints(app, blueprints)

    return app


def register_blueprints(app, import_names):
    blueprints = [import_string(n) for n in import_names]
    for bp in blueprints:
        app.register_blueprint(bp)
    return blueprints
