# -*- coding: UTF-8 -*-
# oauth.rb
#
# OAuth and some twitter action

import tweepy
import yaml

def oauth(conffile):
    # load config file
    string = open(conffile).read()
    string = string.decode('utf8')
    config = yaml.load(string)
    tokens = config['tokens']

    auth = tweepy.OAuthHandler(
            tokens['consumer_key'],
            tokens['consumer_secret']
            )
    auth.set_access_token(
            tokens['access_token'],
            tokens['access_secret']
            )
    return tweepy.API(auth)
