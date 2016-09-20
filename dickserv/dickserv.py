#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3
# https://github.com/acidvegas/dickserv
# dickserv.py

import os
import sys

sys.dont_write_bytecode = True
os.chdir(sys.path[0] or '.')
sys.path += ('core', 'modules')

import debug
import irc

debug.info()
if not debug.check_version(3):
    debug.error_exit('DickServ requires Python 3!')
if debug.check_windows():
    debug.error_exit('DickServ can not be executed on a Windows OS!')
if debug.check_root():
    debug.error_exit('Do not run DickServ as root!')
debug.check_libs()
debug.load_reminders()
irc.DickServ.startup()
debug.keep_alive()
