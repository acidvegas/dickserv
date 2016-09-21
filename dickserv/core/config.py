#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3
# https://github.com/acidvegas/dickserv
# config.py

import inspect
import os

# Connection
server   = 'irc.server.com'
port     = 6667
use_ipv6 = False
use_ssl  = False
vhost    = None
password = None
channel  = '#chats'
key      = None

# Identity
nickname = 'DickServ'
username = 'dickserv'
realname = 'DickServ IRC Bot'

# Login
nickserv = None
operserv = None

# Other
admin_host = 'admin.host'
unreal_dir = '~/unreal/' # For running the bot side-by-side with UnrealIRCd. See modules/unreal.py for more information.

# DO NOT EDIT
data_dir   = os.path.join(os.path.dirname(os.path.realpath(inspect.stack()[-1][1])), 'data')
reminders  = []
start_time = 0
