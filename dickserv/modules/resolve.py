#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3
# https://github.com/acidvegas/dickserv/
# resolve.py

import socket

import httplib

def host(ip):
    return socket.gethostbyaddr(ip)[0]

def url(url):
    url = httplib.clean_url(url)
    return socket.gethostbyname(url)
