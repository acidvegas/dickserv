#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3
# https://github.com/acidvegas/dickserv
# unreal.py

'''
This module is to check for updates on the UnrealIRCd.

To enable this module, make the following changes:

core/irc.py      | Add "unreal.loop().start()" into the "def loops(self):" function
core/commands.py | Add "import unreal"
core/config.py   | Add "unreal_dir = '~/CHANGEME'" under the "admin_host" line. (Replace CHANGEME with the directory location.)

To disable this module, undo the changes above.
'''

import threading
import time

import config
import functions
import httplib
import irc

def check_update():
    source = httplib.get_source('https://www.unrealircd.org/docs/FAQ')
    latest = functions.between(source, 'The latest <b>Stable</b> version is <b>', '</b> which was released on ')
    if current_version != latest:
        return latest
    else:
        return False

def current_version():
    version = os.popen('~/unreal/./unrealircd version').read()
    return version[11:].split()[0]

class loop(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            if time.strftime('%I') == 12:
                update = check_update()
                if update:
                    irc.DickServ.sendmsg(config.channel, 'UnrealIRCd version %s has been released.' % update)
            time.sleep(45*60)
