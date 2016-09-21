#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3
# https://github.com/acidvegas/dickserv
# ascii.py

import glob
import os
import random

import config

ascii_dir = os.path.join(config.data_dir, 'ascii')

def read(file_name):
    if file_name == 'random':
        ascii_list = glob.glob(ascii_dir + '/*')
        ascii_file = random.choice(ascii_list)
    else:
        ascii_file = '%s/%s.txt' % (ascii_dir, file_name)
    if os.path.isfile(ascii_file):
        ascii_txt = open(ascii_file, mode='r', encoding='utf8',  errors='replace').readlines()
        if file_name == 'random':
            return ascii_txt + [os.path.basename(ascii_file),]
        else:
            return ascii_txt
    else:
        return False

def delete(file_name):
    ascii_file = '%s/%s.txt' % (ascii_dir, file_name)
    os.remove(ascii_file)

def rename(file_name, new_name):
    ascii_file = '%s/%s.txt' % (ascii_dir, file_name)
    new_file   = '%s/%s.txt' % (ascii_dir, new_name)
    os.rename(ascii_file, new_file)
