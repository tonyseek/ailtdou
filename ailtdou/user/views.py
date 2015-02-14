from flask import Blueprint, url_for, redirect, request
from flask_login import login_user, logout_user

from ailtdou.ext import oauth, db
from ailtdou.user.models import User


bp = Blueprint('user', __name__)
douban = oauth['douban']


@bp.route('/login')
def login():
    callback_url = url_for('.authorized', _external=True)
    return douban.authorize(callback_url)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@bp.route('/login/authorized')
def authorized():
    response = douban.authorized_response()
    if not response:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description'])

    user = User.from_token(response)
    db.session.commit()
    login_user(user, remember=True)

    return redirect(url_for('main.home'))
