#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3
# https://github.com/acidvegas/dickserv/
# dictionary.py

import httplib
import functions

def define(word):
    source  = httplib.get_source('http://www.merriam-webster.com/dictionary/' + word.replace(' ', '%20'))
    results = functions.between(source, '<meta name="description" content="Define {0}: '.format(word), '">')
    if results:
        return results
    else:
        return False
  
def urban(word):
    api = httplib.get_json('http://api.urbandictionary.com/v0/define?term=' + word.replace(' ', '+'))
    if api['result_type'] != 'no_results':
        definition = api['list'][0]['definition']
        return definition
    else:
        return False
