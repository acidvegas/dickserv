#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3
# https://github.com/acidvegas/dickserv/
# unreal.py

import threading
import time

import config
import functions
import httplib
import irc

def check_update():
    source = httplib.get_source('https://www.unrealircd.org/docs/FAQ')
    latest = functions.between(source, 'The latest <b>Stable</b> version is <b>', '</b> which was released on ')
    if config.ircd_version != latest:
        return latest
    else:
        return False

class loop(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            hour   = time.strftime('%I')
            minute = time.strftime('%M')
            if hour == 12 and minute == 00:
                update = check_update()
                if update:
                    irc.DickServ.sendmsg('UnrealIRCd version %s has been released.' % update)
            time.sleep(45)
