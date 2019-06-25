#!/usr/bin/env python
# DickServ IRC Bot - Developed by acidvegas in Python (https://acid.vegas/dickserv)
# functions.py

import datetime
import random
import re
import time

def between(source, start, stop):
	data = re.compile(start + '(.*?)' + stop, re.IGNORECASE|re.MULTILINE).search(source)
	if data:
		return data.group(1)
	else:
		return False

def current_date():
	return time.strftime('%A, %B %d, %Y - %I:%M %p')

def floatint(data):
    if data.isdigit():
        return int(data)
    else:
        return float(data)

def get_date():
	return datetime.date.today().strftime('%m/%d/%Y')

def get_datetime(data):
	return datetime.datetime.strptime(data, '%m/%d/%Y')

def luck(odds):
	if random_int(1,odds) == 1:
		return True
	else:
		return False

def random_int(min, max):
	return random.randint(min, max)

def timespan(date):
	delta = datetime.date(get_date()) - datetime.date(get_datetime(date))
	return delta.days

def trim(data, max_length):
	if len(data) > max_length:
		return data[:max_length] + '...'
	else:
		return data

def uptime(start_time):
	uptime = datetime.datetime(1,1,1) + datetime.timedelta(seconds=time.time() - start_time)
	return f'{uptime.day-1} Days, {uptime.hour} Hours, {uptime.minute} Minutes, {uptime.second} Seconds'