#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3.5
# https://github.com/acidvegas/dickserv/
# ascii.py

import os

def read(file_name):
    ascii_file = '%s/ascii/%s.txt' % (os.getcwd(), file_name)
    if os.path.isfile(ascii_file):
        return open(ascii_file, 'r').readlines()
    else:
        return False
