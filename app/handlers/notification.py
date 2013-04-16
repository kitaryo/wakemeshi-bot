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

        # output formatting
        time = [u"朝食", u"昼食", u"夕食"]
        weekdays = [u"月", u"火", u"水", u"木", u"金", u"土", u"日"]

        post = u"{month}月{day}日({week}) {time}:\n{menu}".format(
            month=date.month,
            day=date.day,
            week=weekdays[date.weekday()],
            time=time[type],
            menu=menu.menu[type]
            )

        # debug output
        self.response.out.write(post)

        # tweet
        api = twitter.oauth('config/twitter.yaml')
        api.update_status(post)



app = webapp2.WSGIApplication([
    (r'/notification/?([^/]*)/?', NotificationHandler)
    ], debug=True)
