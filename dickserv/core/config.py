#!/usr/bin/env python
# DickServ IRC Bot - Developed by acidvegas in Python (https://acid.vegas/dickserv)
# config.py

class connection:
	server     = 'irc.server.com'
	port       = 6697
	ipv6       = False
	ssl        = True
	ssl_verify = False
	proxy      = None
	vhost      = None
	channel    = '#chats'
	key        = None

class cert:
	key      = None
	file     = None
	password = None

class ident:
	nickname = 'DickServ'
	username = 'dickserv'
	realname = 'acid.vegas/dickserv'

class login:
	network  = None
	nickserv = None
	operator = None

class settings:
	admin    = 'user@host.name'
	cmd_char = '.'
	log      = False
	modes    = None

class api:
	google_api_key       = 'CHANGEME' # https://console.developers.google.com/
	google_cse_id        = 'CHANGEME' # https://cse.google.com/
	omdbapi_key          = 'CHANGEME' # http://www.omdbapi.com/apikey.aspx
	wolfram_api_key      = 'CHANGEME' # http://products.wolframalpha.com/api/
	wunderground_api_key = 'CHANGEME' # https://www.wunderground.com/weather/api/
