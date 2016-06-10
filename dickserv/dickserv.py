#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3.5
# https://github.com/acidvegas/dickserv/
# dickserv.py

import os
import sys

sys.dont_write_bytecode = True
os.chdir(sys.path[0] or '.')
sys.path += ['core', 'modules']

import debug
import irc

debug.info()
if not debug.get_windows():
    if debug.check_root():
        debug.error_exit('Do not run DickServ as root!')
if not debug.check_version(3,5):
    debug.error_exit('DickServ requires Python 3.5')
irc.DickServ.connect()
debug.keep_alive()
