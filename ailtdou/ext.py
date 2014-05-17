from contextlib import contextmanager

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.oauthlib.client import OAuth
from flask.ext.oauthlib.contrib.apps import douban
from raven.contrib.flask import Sentry


__all__ = ['db', 'login_manager', 'oauth', 'sentry', 'capture_exception']


db = SQLAlchemy()
login_manager = LoginManager()
oauth = OAuth()
sentry = Sentry()

douban.register_to(oauth)


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
