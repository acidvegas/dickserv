#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3
# https://github.com/acidvegas/dickserv
# config.py

import inspect
import os

# IRC Settings
server   = 'localhost'
port     = 6697
channel  = '#dev'
password = 'CHANGEME'

# Other Settings
admin_host = 'admin.host'

# DO NOT EDIT
data_dir   = os.path.join(os.path.dirname(os.path.realpath(inspect.stack()[-1][1])), 'data')
last_time  = 0
start_time = 0
reminders  = []
