# mention.py
#
# parse mentions and reply a certain menu
from lib import oauth as twitter

import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db


class LastMention(db.Model):
  id = db.IntegerProperty()
  date = db.DateTimeProperty(auto_now_add=True)

class MentionJob(webapp.RequestHandler):
  def get(self):
    api = twitter.oauth()

    last_mention = db.GqlQuery("SELECT * FROM LastMention LIMIT 1")
    mentions = api.GetMentions(last_mention.id, None, 30)
    print mentions[0].id
    last_mention.id = mentions[0].id
    last_mention.put()

    self.response.out.write("This is cron job on GAE - dev.")

application = webapp.WSGIApplication([('/mention', MentionJob)], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
