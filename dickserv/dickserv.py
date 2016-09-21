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
    if debug.check_admin():
        debug.error_exit('Do not run DickServ as an administrator!')
else:
    if debug.check_root():
        debug.error_exit('Do not run DickServ as root!')
debug.check_libs()
irc.DickServ.connect()
