from flask import Blueprint, url_for, redirect
from flask.ext.login import login_user, logout_user
from flask.ext.oauthlib.client import OAuthException

from ailtdou.ext import oauth, db
from ailtdou.user.models import User, AccessDenied, AccessTokenExpired


bp = Blueprint('user', __name__)


@bp.app_errorhandler(AccessTokenExpired)
def access_token_expired(error):
    user = User.query.get(error.user_id)
    if not user:
        raise RuntimeError('user not found %d' % error.user_id)
    logout_user()
    return redirect(url_for('.login'))


@bp.route('/login')
def login():
    url = url_for('.authorized', _external=True)
    return oauth.douban.authorize(callback=url)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@bp.route('/login/authorized')
@oauth.douban.authorized_handler
def authorized(response):
    try:
        user = User.from_oauth(response)
    except AccessDenied as e:
        return 'Access denied: reason=%s error=%s' % (
            e.reason, e.description)
    except OAuthException as e:
        return 'Authorize Error: %s' % response.message

    db.session.commit()
    login_user(user, remember=True)

    return redirect(url_for('main.home'))
