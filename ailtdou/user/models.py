from flask import request, current_app
from flask.ext.login import UserMixin, current_user
from flask.ext.oauthlib.client import OAuthException

from werkzeug.utils import cached_property
from hashids import Hashids

from ailtdou.ext import db, oauth, login_manager


class User(UserMixin, db.Model):
    """The user account entity."""

    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.Unicode, nullable=False)
    user_info_url = 'user/~me'
    statuses_url = 'https://api.douban.com/shuo/v2/statuses/'

    @cached_property
    def user_info(self):
        response = oauth.douban.get(
            self.user_info_url, token=(self.access_token, ''))
        if response.status == 200:
            return response.data
        # 106 means access_token_has_expired
        if response.data.code == 106:
            raise AccessTokenExpired(
                response.message, response.type, response.data, self.id)
        raise OAuthException('invalid response')

    @property
    def uid(self):
        return self.user_info['uid']

    @property
    def name(self):
        return self.user_info['name']

    @property
    def description(self):
        return self.user_info['desc']

    def get_avatar_url(self, size='normal'):
        if size == 'normal':
            return self.user_info['avatar']
        if size == 'large':
            return self.user_info['large_avatar']
        raise ValueError('%r is not valid size' % size)

    @classmethod
    def from_oauth(cls, response):
        if response is None:
            raise AccessDenied(
                request.args['error_reason'],
                request.args['error_description'])

        if isinstance(response, OAuthException):
            raise response

        user_id = response['douban_user_id']
        access_token = response['access_token']

        user = cls.query.get(user_id)
        if user:
            user.access_token = access_token
        else:
            user = cls(id=user_id, access_token=access_token)
            db.session.add(user)

        return user

    @cached_property
    def secret_id(self):
        hashids = Hashids(current_app.secret_key)
        return hashids.encrypt(self.id)

    @classmethod
    def from_secret_id(cls, secret_id):
        hashids = Hashids(current_app.secret_key)
        unpacked_data = hashids.decrypt(secret_id)
        if len(unpacked_data) != 1:
            return
        return cls.query.get(unpacked_data[0])

    def post_to_douban(self, text):
        text = text.strip()
        data = {'source': oauth.douban.consumer_key, 'text': text}
        return oauth.douban.post(
            self.statuses_url, data=data, token=(self.access_token, ''))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@oauth.douban.tokengetter
def get_douban_access_token():
    if current_user.is_anonymous():
        return
    return current_user.access_token, ''


class AccessDenied(Exception):
    """The exception for access denied."""

    def __init__(self, reason, description):
        self.reason = reason
        self.description = description


class AccessTokenExpired(OAuthException):
    """The access token has expired."""

    def __init__(self, message, type, data, user_id):
        super(AccessTokenExpired, self).__init__(message, type, data)
        self.user_id = user_id
