from flask_wtf import Form
from flask_wtf.html5 import EmailField
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email

class EmailResponse(Form):
  email = EmailField(label=u'recipient', validators=[Email()])
  email_subject = StringField(u'subject', validators=[DataRequired()])
  email_body = TextAreaField(u'body', validators=[DataRequired()])


class IgnorePosting(Form):
  pass


class ConfirmSendEmail(Form):
  pass
