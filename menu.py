# -*- coding: UTF-8 -*-
# menu.py
#
# get menues from wakeijuku.org


import webapp2
from google.appengine.ext import db

import urllib2 as urllib
import lxml.html
import re


url1 = "http://www.wakei.org/jukusei/index.html"
url2 = "http://www.wakei.org/jukusei/index2.html"

class Menu(db.Model):
  date = db.DateProperty()
  type = db.IntegerProperty()
  menu = db.StringProperty(multiline=True)


class MenuParser:
    def get(self):
        list = self.retrieve(url1) + self.retrieve(url2)
        return list

    def retrieve(self, url):
        list = []
        html = urllib.urlopen(url).read()
        html = re.sub(r'</?br\s?/?>', '\n', html)
        doc = lxml.html.fromstring(html)

        for item in doc.xpath("//tbody//tr//td"):
            list.append(item.text)

        return list


class MainPage(webapp2.RequestHandler):
    def get(self):
        menu = MenuParser()
        self.response.headers["Content-Type"] = "text/html; charset=utf-8"
        self.response.out.write(menu.get()[3])

app = webapp2.WSGIApplication([
    ("/menu", MainPage)
    ], debug=True)
