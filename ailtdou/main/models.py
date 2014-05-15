from datetime import datetime
from email import message_from_string
from email.utils import parseaddr
from quopri import decodestring as quopri_decode

from inbox import Inbox
from jinja2.filters import do_striptags as striptags

from ailtdou.ext import db, capture_exception
from ailtdou.user.models import User


class Activity(db.Model):
    """The service activity log."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.id))
    subject = db.Column(db.Unicode(60))
    text = db.Column(db.UnicodeText)
    time = db.Column(db.DateTime, default=datetime.now)


inbox = Inbox()


@inbox.collate
def email_to_douban(to, sender, body):
    with capture_exception(reraise=False):
        _, address = parseaddr(to)
        secret_id, _ = address.rsplit('@', 1)
        user = User.from_secret_id(secret_id)
        if not user:
            return

        message = message_from_string(body)
        try:
            text = extract_text(message)
        except ValueError:
            return

        # save to database
        activity = Activity(user_id=user.id, subject='unknown', text=text)
        db.session.add(activity)
        db.session.commit()
        # post with Douban API
        user.post_to_douban(text[:140])


def extract_text(message):
    if message.is_multipart():
        payload_list = message.get_payload()

        text_payload_list = (
            p for p in payload_list if p.get_content_type() == 'text/plain')
        rich_payload_list = (
            p for p in payload_list if p.get_content_type() == 'text/html')

        chosen = next(text_payload_list, next(rich_payload_list, None))
        if not chosen:
            raise ValueError('unknown content type in message')
    else:
        chosen = message

    payload = chosen.get_payload()
    if chosen.get_content_type() == 'text/html':
        payload = quopri_decode(payload)

    text = payload.decode(chosen.get_content_charset())
    if chosen.get_content_type() == 'text/html':
        text = striptags(text)

    return text
