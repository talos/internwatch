from flask import current_app

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from html2text import html2text


def send_email(toaddr, subject, html):
  html = html.encode('ascii', "xmlcharrefreplace")

  # TODO deleteme
  toaddr = 'irving.krauss@gmail.com'

  config = current_app.config

  # Create message container - the correct MIME type is multipart/alternative.
  msg = MIMEMultipart('alternative')
  msg['Subject'] = subject
  msg['From'] = config['EMAIL_FROM']
  msg['To'] = toaddr

  server = smtplib.SMTP_SSL(config['EMAIL_SERVER'])
  current_app.logger.info(u'Logging in to SMTP {} as {}'.format(
    config['EMAIL_SERVER'], config['EMAIL_USERNAME']))
  server.login(config['EMAIL_USERNAME'], config['EMAIL_PASSWORD'])

  # Record the MIME types of both parts - text/plain and text/html.
  part1 = MIMEText(html2text(html), 'plain')
  part2 = MIMEText(html, 'html')

  msg.attach(part1)
  msg.attach(part2)

  current_app.logger.info(u'Sending mail to {}: {}'.format(
    toaddr, msg.as_string()))
  server.sendmail(config['EMAIL_FROM'], toaddr, msg.as_string())

  try:
    current_app.logger.info(u'Quitting SMTP server')
    server.quit()
  except Exception as e:
    current_app.logger.warn(u"Couldn't quit SMTP server: {}".format(e))
