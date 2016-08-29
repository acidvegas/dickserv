#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3
# https://github.com/acidvegas/dickserv/
# debug.py

import datetime
import os
import threading
import time

import config
import irc

reminder_file = os.getcwd() + '/data/reminders.txt'

class loop(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            reminders = config.reminders
            if reminders:
                date = datetime.datetime.now()
                date = '%d/%d-%d:%d' % (date.month, date.day, date.hour, date.minute)
                for i in reminders:
                    rdate = i.split('|')[0]
                    rnick = i.split('|')[1]
                    rtext = i.split('|')[2]
                    if rdate == date:
                        irc.DickServ.sendmsg('[%s] %s, %s' % (irc.color('R', irc.pink), rnick, rtext))
                        config.reminders.remove(i)
                        sync()
                time.sleep(60)
            else:
                time.sleep(60*19)

def add(nick, duration, type, text):
    if   type == 'm': date = datetime.datetime.now() + datetime.timedelta(minutes=duration)
    elif type == 'h': date = datetime.datetime.now() + datetime.timedelta(hours=duration)
    elif type == 'd': date = datetime.datetime.now() + datetime.timedelta(days=duration)
    date = '%d/%d-%d:%d' % (date.month, date.day, date.hour, date.minute)
    config.reminders.append('%s|%s|%s' % (date, nick, text))
    sync()

def sync():
    config.reminders.sort()
    with open(reminder_file, 'w') as r:
        for item in config.reminders:
            r.write(item + '\n')