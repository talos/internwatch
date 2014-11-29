from flask.ext.script import Manager

from app import app
from internwatch.models import db, Posting, CachedFeed

import feedparser
import requests
import time
from urlparse import urljoin
from bs4 import BeautifulSoup
from time import mktime
from datetime import datetime, date


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
  today = date.today()
  url = 'https://newyork.craigslist.org/search/jjj?query=unpaid&sort=rel&format=rss'

  cached_feed = CachedFeed.query.filter_by(rss_url=url, date=today).first()
  if not cached_feed:
    resp = requests.get(url)
    cached_feed = CachedFeed(rss_url=url, text=resp.text)
    db.session.add(cached_feed)
    db.session.commit()

  feed = feedparser.parse(cached_feed.text)

  for entry in feed.entries:
    link = entry['link']

    # Skip postings that already exist when scanning
    posting = Posting.query.filter_by(url=link, rss_url=url).first()
    if posting:
      continue

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

    print(u"finished {}, sleeping".format(link))
    time.sleep(15)

  db.session.commit()


if __name__ == "__main__":
  manager.run()
