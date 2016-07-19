#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3
# https://github.com/acidvegas/dickserv/
# ascii.py

import glob
import os
import random

ascii_dir = os.getcwd() + '/data/ascii'

def read(file_name):
    if file_name == 'random':
        ascii_list = glob.glob(ascii_dir + '/*')
        ascii_file = random.choice(ascii_list)
    else:
        ascii_file = '%s/%s.txt' % (ascii_dir, file_name)
    if os.path.isfile(ascii_file):
        return open(ascii_file, 'r').readlines()
    else:
        return False
