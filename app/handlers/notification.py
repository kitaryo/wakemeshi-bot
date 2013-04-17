# -*- coding: utf-8 -*-
# notification.py
#
# notify menues periodically


import webapp2

import logging
import datetime
import lib.twitter as twitter
import lib.config
import lib.tweepy as tweepy

# use models
from app.models.menu import Menu

class NotificationHandler(webapp2.RequestHandler):
    def get(self, type=0):
        # normalize input
        if type == "" or type == None:
            type = 0
        type = int(type)
        if (type < 0 and 2 < type):
            type = 0

        # get menu by JST
        date = (datetime.datetime.now() + datetime.timedelta(hours=+9)).date()
        menu = Menu.get_by_key_name(str(date))

        post = menu.format(date, type)

        # debug output
        self.response.out.write(post)

        # tweet
        config = lib.config.load("config/twitter.yaml")
        try:
            api = twitter.oauth(config['tokens'])
            api.update_status(post)
        except tweepy.TweepError, e:
            logging.info(u"Error while updating; {error}".format(error=e.message))



app = webapp2.WSGIApplication([
    (r'/notification/?([^/]*)/?', NotificationHandler)
    ], debug=True)
