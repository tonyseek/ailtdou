from datetime import datetime
from email.utils import parseaddr

from inbox import Inbox

from ailtdou.ext import db
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
def email_to_douban(to, sender, subject, body):
    _, address = parseaddr(to)
    secret_id, _ = address.rsplit('@', 1)
    user = User.from_secret_id(secret_id)
    if user:
        text = body.strip()[:140]
        # save to database
        activity = Activity(user_id=user.id, subject=subject, text=text)
        db.session.add(activity)
        db.session.commit()
        # post with Douban API
        user.post_to_douban(text)
