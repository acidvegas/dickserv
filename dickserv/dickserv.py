#!/usr/bin/env python
# DickServ IRC Bot - Developed by acidvegas in Python (https://acid.vegas/dickserv)
# dickserv.py

import os
import sys

sys.dont_write_bytecode = True
os.chdir(sys.path[0] or '.')
sys.path += ('core','modules')

import debug

debug.setup_logger()
debug.info()
if not debug.check_version(3):
	debug.error_exit('Python 3 is required!')
if debug.check_privileges():
	debug.error_exit('Do not run as admin/root!')
debug.check_libs()
import database
database.check()
import irc
irc.DickServ.connect()