# -*- coding: utf-8 -*-
# mention.py
#
# parse mentions and reply a certain menu

import webapp2
import re
import datetime

import lib.twitter as twitter


# use model
from app.models.menu import Menu
from app.models.mention import Mention

class MentionHandler(webapp2.RequestHandler):
    REP_TYPE_MENU = 0x00
    REP_TYPE_FB   = 0x01
    REP_TYPE_NONE = 0x02
    MENU_TIME_BREAKFAST = 0
    MENU_TIME_LUNCH     = 1
    MENU_TIME_DINNER    = 2
    api = None

    def get(self):
        # instansiate and login to twitter
        self.api = twitter.oauth("config/twitter.yaml")

        # determin which mention is to be processed
        last_mention = Mention.get_or_insert("last_mention")
        since_id = last_mention.id

        # get actual mentions
        mentions = self.api.mentions_timeline(since_id=since_id, count=30)
        if len(mentions) > 0:
            for s in mentions:
                # process against each mention
                self.process(s)

            # update the mark
            last_mention.id = int(mentions[0].id)
            #self.response.out.write(str(mentions[0].id))
            last_mention.put()

    def process(self, status):
        # decide what to do
        rep_type = self.parse_reply_type(status.text)

        if rep_type == self.REP_TYPE_FB:
            # Quoted RT
            self.api.update_status("RT @{name}: {text}".format(
                name=status.user.screen_name,
                text=status.text
                ))

        elif rep_type == self.REP_TYPE_MENU:
            # parse date
            date, time = self.parse_datetime(status.text)
            menu = Menu.get_by_key_name(str(date))

            if menu:
                post = u"@{name} {menu}".format(
                        name=status.user.screen_name,
                        menu=menu.format(date, time))
                self.api.update_status(post,
                        in_reply_to_status_id=status.id
                        )

    def parse_reply_type(self, text):
        # decide what to do
        if re.search(u'朝|昼|夕|夜|明日|明後日|？|何|なに|\\?', text, re.U):
            return self.REP_TYPE_MENU
        elif re.search(u"好|味|良|美|微妙|当たり|あたり|アタリ|ハズレ|はずれ",text, re.U):
            return self.REP_TYPE_FB
        else:
            return self.REP_TYPE_NONE

    def parse_datetime(self, text):
        # current datetime in JST
        t = (datetime.datetime.now() + datetime.timedelta(hours=+9)).date()

        delta = 0
        # parse date
        if re.search(u'一昨日|おととい|いっさくじつ', text, re.U):
            delta = -2
        elif re.search(u'昨日|きのう|さくじつ', text, re.U):
            delta = -1
        elif re.search(u'今日|本日', text, re.U):
            delta = 0
        elif re.search(u'明日|あす|あした', text, re.U):
            delta = 1
        elif re.search(u'明後日|あさって', text, re.U):
            delta = 2
        elif re.search(u'明々後日|明明後日|しあさって', text, re.U):
            delta = 3
        date = t - datetime.timedelta(days=delta)

        res = re.search(u'(?P<day>\d+)日', text, re.U)
        if res:
            d = int(res.group('day').encode('utf-8'))

            res = re.search(u'(?P<month>\d+)月', text, re.U)
            if res:
                m = int(res.group('month').encode('utf-8'))
            elif d < t.day:
                m = t.month + 1
            else:
                m = t.month

            res = re.search(u'(?P<year>\d+)年', text, re.U)
            if res:
                y = int(res.group('year').encode('utf-8'))
            elif m < t.month:
                y = t.year + 1
            else:
                y = t.year

            date = datetime.date(year=y,month=m,day=d)


        # parse time
        if re.search(u'朝', text, re.U):
            return date, self.MENU_TIME_BREAKFAST
        elif re.search(u'昼|ランチ', text, re.U):
            return date, self.MENU_TIME_LUNCH
        else:
            return date, self.MENU_TIME_DINNER



app = webapp2.WSGIApplication([
    (r'/mention', MentionHandler)
    ], debug=True)
