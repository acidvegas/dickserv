#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3.5
# https://github.com/acidvegas/dickserv/
# dictionary.py

import httplib
import functions

def scrabble(word):
    data    = httplib.data_encode({'dictWord' : word})
    source  = httplib.get_source('http://scrabble.hasbro.com/en-us/tools#dictionary', data.encode('ascii'))
    results = functions.between(source, '<strong class="roboto">', '</strong>')
    if results:
        if results == 'CONGRATULATIONS!':
            source     = source.replace('\t', '').replace('\n', '')
            definition = functions.between(source, '<h4>%s</h4>' % word.upper(), '<p>Related Words:')
            return definition
        elif results == 'SORRY. NO RESULT.':
            return False
  
def urban(word):
    api = httplib.get_json('http://api.urbandictionary.com/v0/define?term=' + word.replace(' ', '+'))
    if api['result_type'] != 'no_results':
        definition = api['list'][0]['definition']
        return definition
    else:
        return False
