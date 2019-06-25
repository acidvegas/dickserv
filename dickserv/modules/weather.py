#!/usr/bin/env python
# DickServ IRC Bot - Developed by acidvegas in Python (https://acid.vegas/dickserv)
# weather.py

import httplib

import config

def lookup(zip_code):
	api = httplib.get_json('http://api.wunderground.com/api/{0}/conditions/q/{1}.json'.format(config.api.wunderground_api_key, zip_code))
	if 'error' not in api:
		city    = api['current_observation']['display_location']['city']
		state   = api['current_observation']['display_location']['state']
		country = api['current_observation']['display_location']['country']
		weather = api['current_observation']['weather']
		temp    = api['current_observation']['temp_f']
		return 'The weather for {0}, {1}, {2} is {3} at {4} F'.format(city, state, country, weather, temp)
	else:
		return False
