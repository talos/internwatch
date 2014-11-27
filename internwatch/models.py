from flask.ext.sqlalchemy import SQLAlchemy

from internwatch.forms import EmailResponse

from datetime import datetime, date


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

  def modify_email(self, new_subject, new_body, new_email):
    self.email = new_email
    self.email_subject = new_subject
    self.email_body = new_body

  def send_email(self):
    self.email_sent_at = datetime.now()

  def ignore(self):
    self.ignored_at = datetime.now()

  @property
  def email_response_form(self):
    form = EmailResponse(obj=self)
    return form

  @property
  def status(self):
    if self.email_sent_at:
      return self.Status.SENT
    if self.ignored_at:
      return self.Status.IGNORED
    return self.Status.PENDING

  @classmethod
  def pending(cls, **kwargs):
    return cls.query.filter_by(ignored_at=None, email_sent_at=None, **kwargs)


class CachedFeed(db.Model):

  id = db.Column(db.Integer, primary_key=True)

  date = db.Column(db.Date, default=date.today())

  rss_url = db.Column(db.Text())
  text = db.Column(db.Text())
