# -*- coding: utf-8 -*-
# menu.py
#
# get menues from wakeijuku.org


import webapp2

import urllib2 as urllib
import lxml.html
import re
import datetime

from app.models.menu import Menu

url1 = "http://www.wakei.org/jukusei/index.html"
url2 = "http://www.wakei.org/jukusei/index2.html"

class MenuHandler(webapp2.RequestHandler):
    def get(self):
        self.update()
        items = Menu.query("SELECT * FROM Menu ORDER BY date DESC LIMIT 14")
        for i in items:
            self.response.out.write(u'<p>')
            self.response.out.write(u'%d月%d日<br>' % (i.date.month, i.date.day))
            self.response.out.write(u'朝食: %s<br>' % i.menu[0])
            self.response.out.write(u'昼食: %s<br>' % i.menu[1])
            self.response.out.write(u'夕食: %s<br>' % i.menu[2])
            self.response.out.write(u'</p>')


    def update(self):
        list = self.retrieve(url1) + self.retrieve(url2)

        for i in range(len(list) / 4):
            d = self.parseDate(list[i*4])
            menu = Menu(date=d, key_name=str(d))
            menu.menu = [list[i*4+1], list[i*4+2], list[i*4+3]]
            menu.last_update = datetime.datetime.now().date()
            menu.put()


    def retrieve(self, url):
        list = []
        bytestring = urllib.urlopen(url).read() # returned as a byte string
        # return/break replacement
        bytestring = re.sub(r'</?br\s?/?>', '\n', bytestring) # "re" can handle both unicode string and byte string
        doc = lxml.etree.fromstring(bytestring,
                lxml.etree.HTMLParser(encoding="shift_jis",recover=True))

        for item in doc.xpath('//tbody//tr//td'):
            list.append(item.text)

        return list


    def parseDate(self, datestring):
        t = datetime.datetime.now().date()
        y = t.year

        r = u'(?P<month>\d+)月(?P<day>\d+)日'
        res = re.search(r, datestring, re.U)
        m = int(res.group('month').encode('utf-8'))
        d = int(res.group('day').encode('utf-8'))

        if t.month == 12 and m == 1:
            y = t.year + 1

        return datetime.date(year=y,month=m,day=d)


app = webapp2.WSGIApplication([
    ("/menu", MenuHandler)
    ], debug=True)
