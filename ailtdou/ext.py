from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_oauthlib.client import OAuth
from flask_oauthlib.contrib.apps import douban
from raven.contrib.flask import Sentry


__all__ = ['db', 'login_manager', 'oauth', 'sentry', 'capture_exception']


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
oauth = OAuth()
sentry = Sentry()

douban.register_to(oauth, scope=[
    'douban_basic_common',
    'shuo_basic_r',
    'shuo_basic_w'])


@contextmanager
def capture_exception(*exceptions, **kwargs):
    exceptions = exceptions or (Exception,)
    reraise = kwargs.get('reraise', True)
    try:
        yield
    except exceptions:
        sentry.captureException()
        if reraise:
            raise
