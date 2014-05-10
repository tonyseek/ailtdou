from flask import Blueprint, render_template, session

from ailtdou.ext import oauth


bp = Blueprint('main', __name__)


@bp.route('/')
def home():
    if 'douban_token' in session:
        user = oauth.douban.get('user/~me')
        return render_template('user.html', user=user)
    return render_template('login.html')
