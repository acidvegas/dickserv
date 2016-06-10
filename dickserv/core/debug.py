#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3.5
# https://github.com/acidvegas/dickserv/
# debug.py

import datetime
import os
import sys

def action(msg):
    print('%s | [#] - %s' % (time(), msg))

def alert(msg):
    print('%s | [+] - %s' % (time(), msg))

def check_root():
    if os.getuid() == 0 or os.geteuid() == 0:
        return True
    else:
        return False
    return False
    
def check_version(major, minor):
    if sys.version_info.major == major and sys.version_info.minor == minor:
        return True
    else:
        return False
    
def clear():
    if get_windows():
        os.system('cls')
    else:
        os.system('clear')

def error(msg, reason=None):
    if reason : print('%s | [!] - %s (%s)' % (time(), msg, str(reason)))
    else      : print('%s | [!] - %s'      % (time(), msg))

def error_exit(msg):
    raise SystemExit('%s | [!] - %s' % (time(), msg))

def get_windows():
    if os.name == 'nt':
        return True
    else:
        return False

def info():
    clear()
    print(''.rjust(56, '#'))
    print('#' + ''.center(54) + '#')
    print('#' + 'DickServ IRC Bot'.center(54) + '#')
    print('#' + 'Developed by ak in Python 3.5'.center(54) + '#')
    print('#' + 'https://github.com/acidvegas/dickserv/'.center(54) + '#')
    print('#' + ''.center(54) + '#')
    print(''.rjust(56, '#'))

def help():
    return '''
@help               Information about the commands.
.ascii list         A list of all the ASCII art files.
.ascii <name>       Display the <name> ASCII art file.
.btc                Bitcoin rate in USD.
.date               Get the current date and time.
.define <word>      Get the definition of <word>.
.dickserv           Information about the bot.
.fml                Random \'FuckMyLife\' story.
.imdb <query>       Search IMDb and return the 1st result for <search>.
.isup <url>         Check if <url> is up or not.
.ltc                Litecoin rate in USD.
.reddit <subreddit> Read top posts from <subreddit>
.talent             RIP DITTLE DIP DIP DIP DIP IT\'S YA BIRTHDAY!!1@11!
.ud <word>          Get the urban dictionary definition of <word>.
.uptime             Get the amount of time DickServ has been running.
.wolfram <ask>      Get the results of <query> from WolframAlpha.
.yt <query>         Search <query> on YouTube.
    '''

def irc(msg):
    print('%s | [~] - %s' % (time(), msg))

def keep_alive():
    try:
        while True : input('')
    except KeyboardInterrupt:
        sys.exit()

def time():
    return datetime.datetime.now().strftime('%I:%M:%S')
