# -*- coding: UTF-8 -*-
# config.rb
#
# Config loader

import yaml

def load(conffile):
    string = open(conffile).read()
    string = string.decode('utf8')
    return yaml.load(string)
