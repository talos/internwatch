from flask.ext.sqlalchemy import SQLAlchemy

from internwatch.forms import EmailResponse
from internwatch.utils import send_email

from datetime import datetime, date
import re


db = SQLAlchemy()


class Posting(db.Model):

  class Status:
    PENDING, IGNORED, SENT = ('pending', 'ignored', 'sent')

  id = db.Column(db.Integer, primary_key=True)

  title = db.Column(db.String())
  url = db.Column(db.Text())
  rss_url = db.Column(db.Text())
  text = db.Column(db.Text())
  region = db.Column(db.Text())

  posted_at = db.Column(db.DateTime())
  created_at = db.Column(db.DateTime(), default=datetime.now)

  email = db.Column(db.Text())
  email_subject = db.Column(db.Text())
  email_body = db.Column(db.Text())
  email_sent_at = db.Column(db.DateTime())

  ignored_at = db.Column(db.DateTime())

  email_responded_at = db.Column(db.DateTime())
  posted_online_at = db.Column(db.DateTime())

  def send_email(self):
    if self.can_send:
      send_email(self.email, self.email_subject, self.email_body)
      self.email_sent_at = datetime.now()
    else:
      pass

  def ignore(self):
    self.ignored_at = datetime.now()

  def unignore(self):
    self.ignored_at = None

  @property
  def text_stripped(self):
    """Strip erroneous linebreak close tags"""
    return re.sub(r'</br[^>]*>', '', self.text)

  @property
  def can_send(self):
    return self.email and self.email_subject and self.email_body and \
        not self.email_sent_at

  @property
  def email_response_form(self):
    return EmailResponse(obj=self)

  @property
  def status(self):
    if self.ignored_at:
      return self.Status.IGNORED
    if self.email_sent_at:
      return self.Status.SENT
    return self.Status.PENDING

  @classmethod
  def all_with_status(cls, status):
    for m in cls.query.all():
      if m.status == status:
        yield m


class CachedFeed(db.Model):

  id = db.Column(db.Integer, primary_key=True)

  date = db.Column(db.Date, default=date.today())

  rss_url = db.Column(db.Text())
  text = db.Column(db.Text())
