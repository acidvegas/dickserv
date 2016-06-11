#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3.5
# https://github.com/acidvegas/dickserv/
# wolfram.py

from xml.etree import ElementTree as etree

import httplib

def ask(query):
    params  = httplib.data_encode({'input':query, 'appid':'95HYLQ-3GQRHUEKT6'})
    data    = httplib.get_source('http://api.wolframalpha.com/v2/query?' + params)
    results = {}
    tree    = etree.fromstring(data)
    for e in tree.findall('pod'):
        for item in [ef for ef in list(e) if ef.tag=='subpod']:
            for it in [i for i in list(item) if i.tag=='plaintext']:
                if it.tag=='plaintext':
                    results[e.get('title')] = it.text
    if 'Result' in results:
        return results['Result']
    else:
        return False
