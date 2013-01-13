# -*- coding: UTF-8 -*-
# menu.py
#
# get menues from wakeijuku.org

import urllib2 as urllib
from pyquery import PyQuery as pq
from lxml import html


url1 = "http://www.wakei.org/jukusei/index.html"
url2 = "http://www.wakei.org/jukusei/index2.html"

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
