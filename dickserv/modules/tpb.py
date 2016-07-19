#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3
# https://github.com/acidvegas/dickserv/
# tpb.py

import re

import httplib

def search(query):
    url      = 'https://thepiratebay.org/search/' + query.replace(' ', '+') + '/0/99/0'
    source   = httplib.get_source(url)
    torrents = re.findall('<a href="(.*?)" class="detLink".*>(.*?)</a>', source)
    seeders  = re.findall('\t\t</td>\n\t\t<td align="right">(.*?)</td>', source)
    leechers = re.findall('<td align="right">(.*?)</td>\n\t</tr>',       source)
    if torrents:
        results = {}
        if len(torrents) > 10:
            torrents = torrents[:10]
        for i in range(len(torrents)):
            results[torrents[i][1]] = {'seeders':seeders[1], 'leechers':leechers[i], 'url':torrents[i][0]}
        return results
    else:
       return False
