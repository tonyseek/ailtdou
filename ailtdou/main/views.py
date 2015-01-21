from flask import Blueprint, render_template
from flask_login import current_user


bp = Blueprint('main', __name__)


@bp.route('/')
def home():
    if current_user.is_anonymous():
        return render_template('login.html')
    return render_template('user.html', user=current_user)
