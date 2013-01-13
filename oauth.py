# -*- coding: UTF-8 -*-
# oauth.rb
#
# OAuth and some twitter action

import twitter
import yaml

def oauth():
  # load config file
  string = open('twitter.yaml').read()
  string = string.decode('utf8')
  config = yaml.load(string)

  api = twitter.Api(
      consumer_key=str(config['tokens']['consumer_key']),
      consumer_secret=str(config['tokens']['consumer_secret']),
      access_token_key=str(config['tokens']['access_token']),
      access_token_secret=str(config['tokens']['access_secret']),
      cache=None)
  return api

if __name__ == "__main__":
  oauth()
