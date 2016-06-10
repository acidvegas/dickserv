#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3.5
# https://github.com/acidvegas/dickserv/
# cryptocurrency.py

import httplib

def btc():
    api  = httplib.get_json('https://blockchain.info/ticker')
    return '$' + str(api['USD']['15m'])

def ltc():
    api  = httplib.get_json('https://btc-e.com/api/2/ltc_usd/ticker')
    data = str(api['ticker']['last'])
    rate = data.split('.')[0] + '.' + data.split('.')[1][:2]
    return '$' + rate
