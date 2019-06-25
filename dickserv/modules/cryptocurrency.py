#!/usr/bin/env python
# DickServ IRC Bot - Developed by acidvegas in Python (https://acid.vegas/dickserv)
# cryptocurrency.py

import httplib

def get(coin):
	api  = httplib.get_json('https://api.coinmarketcap.com/v1/ticker/?limit=500')
	data = [item for item in api if (coin.lower() == item['id'] or coin.upper() == item['symbol'])]
	if data:
		return data[0]
	else:
		return False