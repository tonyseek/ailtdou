from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.oauthlib.client import OAuth


db = SQLAlchemy()
login_manager = LoginManager()
oauth = OAuth()

# registers OAuth app
oauth.remote_app(
    name='douban',
    app_key='DOUBAN',
    base_url='https://api.douban.com/v2/',
    request_token_params={
        'scope': 'douban_basic_common,shuo_basic_r,shuo_basic_w'},
    access_token_url='https://www.douban.com/service/auth2/token',
    authorize_url='https://www.douban.com/service/auth2/auth',
    access_token_method='POST')
