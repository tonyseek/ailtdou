from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_oauthlib.contrib.client import OAuth
from raven.contrib.flask import Sentry


__all__ = ['db', 'login_manager', 'oauth', 'sentry', 'capture_exception']


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
oauth = OAuth()
sentry = Sentry()

oauth.remote_app(
    name='douban',
    version='2',
    endpoint_url='https://api.douban.com/',
    access_token_url='https://www.douban.com/service/auth2/token',
    refresh_token_url='https://www.douban.com/service/auth2/token',
    authorization_url='https://www.douban.com/service/auth2/auth',
    scope=['douban_basic_common', 'shuo_basic_r', 'shuo_basic_w'],
    compliance_fixes='.douban:douban_compliance_fix')


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
