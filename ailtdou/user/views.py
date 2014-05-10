from flask import Blueprint, url_for, session, redirect
from flask.ext.oauthlib.client import OAuthException

from ailtdou.ext import oauth


bp = Blueprint('user', __name__)


@bp.route('/login')
def login():
    url = url_for('.authorized', _external=True)
    return oauth.douban.authorize(callback=url)


@bp.route('/login/authorized')
@oauth.douban.authorized_handler
def authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description'])
    if isinstance(resp, OAuthException):
        return 'Authorize Error: %s' % resp.message
    session['douban_token'] = (resp['access_token'], '')
    return redirect(url_for('main.home'))


@oauth.douban.tokengetter
def get_douban_oauth_token():
    return session.get('douban_token')
