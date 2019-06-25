#!/usr/bin/env python
# DickServ IRC Bot - Developed by acidvegas in Python (https://acid.vegas/dickserv)
# wolfram.py

from xml.etree import ElementTree as etree

import config
import httplib

def ask(query):
	params  = httplib.data_encode({'input':query, 'appid':config.api.wolfram_api_key})
	data    = httplib.get_source('http://api.wolframalpha.com/v2/query?' + params)
	results = {}
	tree	= etree.fromstring(data)
	for e in tree.findall('pod'):
		for item in [ef for ef in list(e) if ef.tag=='subpod']:
			for it in [i for i in list(item) if i.tag=='plaintext']:
				if it.tag=='plaintext':
					results[e.get('title')] = it.text
	if 'Result' in results:
		return results['Result']
	else:
		return False