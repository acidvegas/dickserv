#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3.5
# https://github.com/acidvegas/dickserv/
# functions.py

import datetime
import random
import re
import time

import config

def between(source, start, stop):
    data = re.compile(start + '(.*?)' + stop, re.IGNORECASE).search(source)
    if data : return data.group(1)
    else    : return False

def date():
    return datetime.datetime.now().strftime('%A, %B %d, %Y - %I:%M %p')

def lucky():
    return random.choice([True, False, False, False])

def random_int(min, max):
    return random.randint(min, max)

def random_str(size):
    return ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', size))

def replacer(source, old, new):
    return re.compile(re.escape(old), re.IGNORECASE).sub(new, source)

def trim(data, max_length):
    if len(data) > max_length:
        return data[:max_length] + '...'
    else:
        return data

def uptime():
    uptime = datetime.datetime(1,1,1) + datetime.timedelta(seconds=time.time() - config.start_time)
    return '%d Days, %d Hours, %d Minutes, %d Seconds' % (uptime.day-1, uptime.hour, uptime.minute, uptime.second)