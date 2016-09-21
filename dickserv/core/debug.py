#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3
# https://github.com/acidvegas/dickserv
# debug.py

import ctypes
import os
import sys
import time

import config

def check_admin():
    if ctypes.windll.shell32.IsUserAnAdmin() != 0:
        return True
    else:
        return False
        
def check_libs():
    try:
        import bs4
    except ImportError:
        error_exit('Missing required \'bs4\' library. (https://pypi.python.org/pypi/beautifulsoup4)')

def check_root():
    if os.getuid() == 0 or os.geteuid() == 0:
        return True
    else:
        return False
    
def check_version(major):
    if sys.version_info.major == major:
        return True
    else:
        return False

def check_windows():
    if os.name == 'nt':
        return True
    else:
        return False
    
def clear():
    if check_windows():
        os.system('cls')
    else:
        os.system('clear')

def error(msg, reason=None):
    if reason:
        print('%s | [!] - %s (%s)' % (get_time(), msg, str(reason)))
    else:
        print('%s | [!] - %s' % (get_time(), msg))

def error_exit(msg):
    raise SystemExit('%s | [!] - %s' % (get_time(), msg))

def get_time():
    return time.strftime('%I:%M:%S')

def info():
    clear()
    print(''.rjust(56, '#'))
    print('#%s#' % ''.center(54))
    print('#%s#' % 'DickServ IRC Bot'.center(54))
    print('#%s#' % 'Developed by acidvegas in Python 3'.center(54))
    print('#%s#' % 'https://github.com/acidvegas/dickserv'.center(54))
    print('#%s#' % ''.center(54))
    print(''.rjust(56, '#'))

def irc(msg):
    print('%s | [~] - %s' % (get_time(), msg))
