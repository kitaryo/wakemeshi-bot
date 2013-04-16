# -*- coding: utf-8 -*-
# notification.py
#
# notify menues periodically


import webapp2

import datetime
import lib.twitter as twitter

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

        # get menu
        date = datetime.datetime.now().date()
        menu = Menu.get_by_key_name(str(date))

        post = menu.format(date, type)

        # debug output
        self.response.out.write(post)

        # tweet
        api = twitter.oauth('config/twitter.yaml')
        api.update_status(post)



app = webapp2.WSGIApplication([
    (r'/notification/?([^/]*)/?', NotificationHandler)
    ], debug=True)
