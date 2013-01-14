# -*- coding: UTF-8 -*-
# menu.py
#
# get menues from wakeijuku.org

import urllib2 as urllib
from pyquery import PyQuery as pq
from lxml import html

import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db


url1 = "http://www.wakei.org/jukusei/index.html"
url2 = "http://www.wakei.org/jukusei/index2.html"

class Greeting(db.Model):
  date = db.DateProperty()
  type = db.IntegerProperty()
  menu = db.StringProperty(multiline=True)


def menu():
  list = parse(url1) + parse(url2)
  print list


def parse(url):
  list = []
  d = pq(url=url)

  for tr in d(".green-table > tbody > tr"):
    tds = pq(tr)("td")

    ar = []
    ar.append(tds.eq(0).text())
    ar.append(tds.eq(1).text())
    ar.append(tds.eq(2).text())
    ar.append(tds.eq(3).text())

    list.append(ar)

  return list


if __name__ == "__main__":
  menu()
