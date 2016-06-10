#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3.5
# https://github.com/acidvegas/dickserv/
# fml.py

import functions
import httplib

def lookup():
    api    = httplib.get_source('http://api.fmylife.com/view/random?language=en&key=53637bae986a8')
    result = functions.between(api, '<text>', '</text>')
    return result
