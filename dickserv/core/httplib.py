#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3
# https://github.com/acidvegas/dickserv/
# httplib.py

import json
import os
import re
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

import functions

def clean_url(url):
    for prefix in ('http://', 'https://', 'www.'):
        url = url.replace(prefix, '', 1)
    if url[-1:] == '/': url = url[:-1]
    return url

def data_quote(data):
    return urllib.parse.quote(data)

def data_encode(data):
    return urllib.parse.urlencode(data)

def get_file(url):
    return os.path.basename(url)

def get_json(url):
    return json.loads(get_source(url))

def get_size(url):
    content_length = int(get_url(url).getheader('content-length'))
    for unit in ('B','KB','MB','GB','TB','PB','EB','ZB'):
        if abs(content_length) < 1024.0:
            return str(content_length) + unit
        content_length /= 1024.0
    return str(content_length) + 'YB'

def get_source(url):
    source  = get_url(url)
    charset = source.headers.get_content_charset()
    if charset:
        return source.read().decode(charset)
    else:
        return source.read().decode()
    
def get_title(url):
    source = get_source(url)
    soup   = BeautifulSoup(source, 'html.parser')
    title  = soup.title.string.replace('\n', '').replace('\t', '')
    return functions.clean_whitespace(title)

def get_type(url):
    return get_url(url).info().get_content_type()

def get_url(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'DickServ/1.0')
    return urllib.request.urlopen(req)

def parse_urls(string):
    return re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.IGNORECASE).findall(string)
