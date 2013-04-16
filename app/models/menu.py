# -*- coding: utf-8 -*-
# menu.py
#
# Model "Menu"

from google.appengine.ext import db

class Menu(db.Model):
    date = db.DateProperty(required=True)
    menu = db.StringListProperty()
    last_update = db.DateProperty()

    def format(self, date, time):
        # output formatting
        time_list = [u"朝食", u"昼食", u"夕食"]
        weekdays = [u"月", u"火", u"水", u"木", u"金", u"土", u"日"]

        return u"{month}月{day}日({week}) {time}:\n{menu}".format(
            month=date.month,
            day=date.day,
            week=weekdays[date.weekday()],
            time=time_list[time],
            menu=self.menu[time]
            )
