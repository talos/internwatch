from flask.ext.sqlalchemy import SQLAlchemy

import datetime


db = SQLAlchemy()


class Posting(db.Model):

  #__tablename__ = 'posting'

  id = db.Column(db.Integer, primary_key=True)

  title = db.Column(db.String())
  url = db.Column(db.Text())
  rss_url = db.Column(db.Text())
  text = db.Column(db.Text())
  region = db.Column(db.Text())

  posted_at = db.Column(db.DateTime())
  created_at = db.Column(db.DateTime(), default=datetime.datetime.now)

  email = db.Column(db.Text())
  email_subject = db.Column(db.Text())
  email_body = db.Column(db.Text())
  email_sent_at = db.Column(db.DateTime())

  ignored_at = db.Column(db.DateTime())

  email_responded_at = db.Column(db.DateTime())
  posted_online_at = db.Column(db.DateTime())

  def send_email(self):
    pass
