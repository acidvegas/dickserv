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
if debug.check_privileges():
    debug.error_exit('Do not run DickServ as admin/root!')
debug.check_libs()
irc.DickServ.connect()
