from flask import current_app
from flask_login import UserMixin, current_user
from flask_oauthlib.contrib.client.structure import OAuth2Response

from werkzeug.utils import cached_property
from hashids import Hashids

from ailtdou.ext import db, oauth, login_manager


douban = oauth['douban']


class User(UserMixin, db.Model):
    """The user account entity."""

    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.Unicode, nullable=False)
    refresh_token = db.Column(db.Unicode, nullable=True)
    user_info_url = 'user/~me'
    statuses_url = 'https://api.douban.com/shuo/v2/statuses/'

    @cached_property
    def user_info(self):
        response = douban.get(
            self.user_info_url, token=(self.access_token, ''))
        if response.status == 200:
            return response.data
        if response.data['code'] == 106:
            raise ValueError('access_token_has_expired', response, self.id)
        raise ValueError('invalid response')

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
        user_id = response['douban_user_id']
        user = cls.query.get(user_id) or cls(id=user_id)
        user.access_token = response.access_token
        user.refresh_token = response.refresh_token
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
        data = {'source': douban.consumer_key, 'text': text}
        return douban.post(
            self.statuses_url, data=data, token=(self.access_token, ''))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@douban.tokengetter
def obtain_token():
    if current_user.is_anonymous():
        return
    return OAuth2Response(
        access_token=current_user.access_token,
        refresh_token=current_user.refresh_token)


@douban.tokensaver
def store_token(token):
    User.from_oauth(token)
    db.session.commit()
