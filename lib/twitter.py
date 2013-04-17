# -*- coding: UTF-8 -*-
# twitter.rb
#
# OAuth and some twitter action

import tweepy

def oauth(tokens):
    auth = tweepy.OAuthHandler(
            tokens['consumer_key'],
            tokens['consumer_secret']
            )
    auth.set_access_token(
            tokens['access_token'],
            tokens['access_secret']
            )
    return tweepy.API(auth)
