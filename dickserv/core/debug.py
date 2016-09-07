#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3
# https://github.com/acidvegas/dickserv/
# debug.py

import os
import sys
import time

import config

def check_libs():
    try                : import bs4
    except ImportError : error_exit('Missing required \'bs4\' library. (https://pypi.python.org/pypi/beautifulsoup4)')

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
    if reason : print('%s | [!] - %s (%s)' % (get_time(), msg, str(reason)))
    else      : print('%s | [!] - %s'      % (get_time(), msg))

def error_exit(msg):
    raise SystemExit('%s | [!] - %s' % (get_time(), msg))

def get_time():
    return time.strftime('%I:%M:%S')

def help():
    return '''@help                 Information about the commands.
.ascii list           A list of all the ASCII art files.
.ascii random         Display a random ASCII art file.
.ascii <name>         Display the <name> ASCII art file.
.btc                  Bitcoin rate in USD.
.date                 Get the current date and time.
.define <word>        Get the definition of <word>.
.dickserv             Information about the bot.
.filter enable        Enable word filters.
.filter disable       Disable word filters.
.geoip <ip>           Geographical location information about <ip>.
.imdb <query>         Search IMDb and return the 1st result for <search>.
.isup <url>           Check if <url> is up or not.
.ltc                  Litecoin rate in USD.
.r <subreddit>        Read top posts from <subreddit>
.remind <time> <text> Remind yourself about <text> in <time>.
.resolve <ip/url>     Resolve <ip/url> to a hostname or IP address.
.steam <query>        Search <query> on the Steam store.
.talent               RIP DITTLE DIP DIP DIP DIP IT\'S YA BIRTHDAY!!1@11!
.tpb <query>          Search <query> on ThePirateBay.
.ud <word>            Get the urban dictionary definition of <word>.
.uptime               Get the amount of time DickServ has been running.
.wolfram <ask>        Get the results of <query> from WolframAlpha.
.yt <query>           Search <query> on YouTube.'''

def info():
    clear()
    print(''.rjust(56, '#'))
    print('#' + ''.center(54) + '#')
    print('#' + 'DickServ IRC Bot'.center(54) + '#')
    print('#' + 'Developed by acidvegas in Python 3'.center(54) + '#')
    print('#' + 'https://github.com/acidvegas/dickserv/'.center(54) + '#')
    print('#' + ''.center(54) + '#')
    print(''.rjust(56, '#'))

def irc(msg):
    print('%s | [~] - %s' % (get_time(), msg))

def keep_alive():
    try:
        while True : input('')
    except KeyboardInterrupt:
        sys.exit()

def load_reminders():
    reminder_file = os.getcwd() + '/data/reminders.txt'
    if os.path.isfile(reminder_file):
        with open(reminder_file, 'r') as r:
            lines = list_file.read().splitlines()
            for line in [x for x in lines if x]:
                config.reminders.append(line)
