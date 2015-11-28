import time
import re

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
    expires_in = db.Column(db.Integer, default=3920)
    expires_at = db.Column(db.Integer, default=0)

    @cached_property
    def user_info(self):
        response = douban.get('v2/user/~me', token=self.token)
        response.raise_for_status()
        return response.json()

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
    def from_token(cls, response):
        user_id = response['douban_user_id']
        user = cls.query.get(user_id) or cls(id=user_id)
        user.access_token = response['access_token']
        user.refresh_token = response['refresh_token']
        user.expires_in = response['expires_in']
        user.expires_at = response['expires_in'] + time.time()
        db.session.add(user)
        return user

    @cached_property
    def token(self):
        return OAuth2Response(
            access_token=self.access_token,
            refresh_token=self.refresh_token,
            expires_at=self.expires_at or -1)

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
        text, tail_link = _extract_tail_link(text)
        data = {'source': douban.client_id, 'text': text}
        if tail_link is not None:
            data['rec_url'] = tail_link
        return douban.post('/shuo/v2/statuses/', data=data, token=self.token)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@douban.tokengetter
def obtain_token():
    if current_user.is_anonymous():
        return
    return current_user.token


@douban.tokensaver
def store_token(token):
    User.from_token(token)
    db.session.commit()


_re_http_url = re.compile(
    r'https?://(?P<host>[^/:]+)(?P<port>:[0-9]+)?(?P<path>\/.*)?')


def _extract_tail_link(text):
    text = unicode(text)
    matched = _re_http_url.search(text)

    # there is not link
    if matched is None:
        return text, None

    # link is not tail
    start, stop = matched.span()
    if len(text) != stop:
        return text, None

    # gotcha
    return text[:start].strip(), text[start:].strip()
