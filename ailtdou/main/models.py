import quopri
import base64
from datetime import datetime
from email import message_from_string
from email.utils import parseaddr

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
        with capture_exception(ValueError):
            text = extract_text(message)
        if not text:
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
            raise ValueError('need plain text or html message')
    else:
        chosen = message

    payload = chosen.get_payload()
    content_charset = chosen.get_content_charset()
    transfer_encoding = chosen.get('Content-Transfer-Encoding')

    # decodes with transfer encoding
    transfer_decoder = {
        'quoted-printable': quopri.decodestring,
        'base64': base64.decodestring,
    }.get(transfer_encoding)
    if transfer_decoder is not None:
        payload = transfer_decoder(payload)
    elif transfer_encoding is not None:
        raise ValueError('unknown transfer encoding in message')

    # decodes to unicode
    text = payload.decode(content_charset)

    # strip html tags
    if chosen.get_content_type() == 'text/html':
        text = striptags(text)

    return text.strip()
