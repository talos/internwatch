from flask_wtf import Form
from flask_wtf.html5 import EmailField
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, ValidationError

import re


class EmailResponse(Form):
  email = EmailField(label=u'recipient', validators=[Email()])
  email_subject = StringField(u'subject', validators=[DataRequired()])
  email_body = TextAreaField(u'body', validators=[DataRequired()])

  def validate_email_body(form, field):
    if re.match('name on posting', field.data, re.I) != -1:
      raise ValidationError(u"Please specify who the message is to (next to 'Dear').")


class IgnorePosting(Form):
  pass


class ConfirmSendEmail(Form):
  pass
