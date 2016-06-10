#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3.5
# https://github.com/acidvegas/dickserv/
# httplib.py

import json
import re
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

def clean_url(url):
    for prefix in ['http://', 'https://', 'www.']:
        url = url.replace(prefix, '', 1)
    return 'http://' + url

def data_quote(data):
    return urllib.parse.quote(data)

def data_encode(data):
    return urllib.parse.urlencode(data)

def get_title(url):
    source = get_source(url)
    soup = BeautifulSoup(source, 'html.parser')
    return soup.title.string.replace('\n', '').replace('\t', '')

def get_source(url, data=None):
    if data : req = urllib.request.Request(url, data)
    else    : req = urllib.request.Request(url)
    req.add_header('User-Agent', 'DickServ/1.0')
    source = urllib.request.urlopen(req)
    charset = source.headers.get_content_charset()
    return source.read().decode(charset)
    
def get_type(url):
    return urllib.request.urlopen(url).info().get_content_type()

def get_json(url):
    return json.loads(get_source(url))

def strip_html(source):
    return re.compile(r'<.*?>').sub('', source)
