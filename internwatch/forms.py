from flask_wtf import Form
from flask_wtf.html5 import EmailField
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email #, ValidationError

#import re


class EmailResponse(Form):
  email = EmailField(label=u'Recipient', validators=[Email()])
  email_subject = StringField(u'Subject', validators=[DataRequired()])
  email_body = TextAreaField(u'Body', validators=[DataRequired()])

  #def validate_email_body(form, field):
  #  if re.match('name on posting', field.data, re.I):
  #    raise ValidationError(u"Please specify who the message is to (next to 'Dear').")


class IgnorePosting(Form):
  pass


class ConfirmSendEmail(Form):
  pass
