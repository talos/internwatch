from flask.ext.script import Manager

from app import app
from internwatch.models import db, Posting

from urlparse import urljoin
from bs4 import BeautifulSoup
import feedparser
import requests
from time import mktime
from datetime import datetime


manager = Manager(app)


@manager.command
def drop_and_create_db():
  db.drop_all()
  db.create_all()


@manager.command
#@manager.option('-u', '--url', dest='url',
                #default='https://newyork.craigslist.org/search/jjj?query=unpaid&sort=rel&format=rss')
def update_db_from_rss():
  """
  Grabs RSS feed from CL and updates DB from it
  """
  url = 'https://newyork.craigslist.org/search/jjj?query=unpaid&sort=rel&format=rss'
  import pdb
  pdb.set_trace()
  feed = feedparser.parse(url)
  for entry in feed.entries[0:2]:
    link = entry['link']
    posting_resp = requests.get(link)
    posting_soup = BeautifulSoup(posting_resp.text)

    replylink = posting_soup.find(id="replylink")
    contact_href = replylink.get('href') if replylink else None

    contact_url = urljoin(url, contact_href)
    contact_resp = requests.get(contact_url)
    contact_soup = BeautifulSoup(contact_resp.text)

    anonemail_el = contact_soup.find(class_="anonemail")

    posting = Posting(title=posting_soup.find('title').text,
                      url=link,
                      rss_url=url,
                      text=unicode(posting_soup.find(id='postingbody')),
                      region='nyc',
                      posted_at = datetime.fromtimestamp(mktime(entry.published_parsed)),
                      email=anonemail_el.text if anonemail_el else None,
                      email_subject='default subject',
                      email_body='default_body')

    db.session.add(posting)

  db.session.commit()


if __name__ == "__main__":
  manager.run()
