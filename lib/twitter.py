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

    auth = tweepy.OAuthHandler(
            str(config['tokens']['consumer_key']),
            str(config['tokens']['consumer_secret'])
            )
    auth.set_access_token(
            str(config['tokens']['access_token']),
            str(config['tokens']['access_secret'])
            )
    return tweepy.API(auth)
