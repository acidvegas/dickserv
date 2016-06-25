#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3.5
# https://github.com/acidvegas/dickserv/
# irc.py

import re
import socket
import ssl
import time

import config
import debug
import functions
import httplib

from commands import *

# Formatting Control Characters / Color Codes
bold        = '\x02'
colour      = '\x03'
italic      = '\x1D'
underline   = '\x1F'
reverse     = '\x16'
reset       = '\x0f'
white       = '00'
black       = '01'
blue        = '02'
green       = '03'
red         = '04'
brown       = '05'
purple      = '06'
orange      = '07'
yellow      = '08'
light_green = '09'
cyan        = '10'
light_cyan  = '11'
light_blue  = '12'
pink        = '13'
grey        = '14'
light_grey  = '15'

def color(msg, foreground, background=None):
    if foreground == 'random' : foreground = '%02d' % functions.random_int(2, 13)
    if background == 'random' : background = '%02d' % functions.random_int(2, 13)
    if background : return '%s%s,%s%s%s' % (colour, foreground, background, msg, reset)
    else          : return '%s%s%s%s'    % (colour, foreground, msg, reset)

class IRC(object):
    def __init__(self, server, port, use_ssl, password, channel, key, nickname, username, realname, nickserv, operserv):
        self.server   = server
        self.port     = port
        self.use_ssl  = use_ssl
        self.password = password
        self.channel  = channel
        self.key      = key
        self.nickname = nickname
        self.username = username
        self.realname = realname
        self.nickserv = nickserv
        self.operserv = operserv
        self.sock     = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.use_ssl : self.sock = ssl.wrap_socket(self.sock)
            self.sock.connect((self.server, self.port))
            if self.password : self.raw('PASS ' + self.password)
            self.raw('USER %s 0 * :%s' % (self.username, self.realname))
            self.nick(self.nickname)
            self.listen()
        except Exception as ex:
            debug.error('Failed to connect to IRC server.', ex)
            self.event_disconnect()
            
    def disconnect(self):
        if self.sock != None:
            try    : self.sock.shutdown(socket.SHUT_RDWR)
            except : pass
            self.sock.close()
            self.sock = None

    def error(self, chan, msg, reason=None):
        if reason : self.sendmsg(chan, '[%s] %s %s' % (color('ERROR', red), msg, color('(' + str(reason) + ')', grey)))
        else      : self.sendmsg(chan, '[%s] %s'    % (color('ERROR', red), msg))
            
    def event_connect(self):
        config.start_time = time.time()
        if self.nickserv : self.identify(self.username, self.nickserv)
        if self.operserv : self.oper(self.nickname, self.oper)
        self.mode(self.nickname, '+B')
        self.join(self.channel, self.key)
        
    def event_disconnect(self):
        self.disconnect()
        time.sleep(5)
        self.connect()
        
    def event_join(self, nick, chan):
        self.sendmsg(chan, '%s %s%s' % (color('SMELLO', 'random'), bold, nick.upper()))
    
    def event_kick(self, nick, chan, kicked, reason):
        if kicked == self.nickname:
            if chan == self.channel:
                self.join(self.channel, self.key)
            else:
                self.join(chan)
        else:
            self.sendmsg(chan, '%s %s%s' % (color('BYE', 'random'), bold, kicked.upper()))

    def event_message(self, nick, host, chan, msg):
        try:
            if not msg.startswith('.'):
                if time.time() - config.last_time > 3:
                    urls = httplib.parse_urls(msg)
                    if urls:
                        config.last_time = time.time()
                        self.event_url(chan, urls[0])
                if   'qhat' in msg                    : self.sendmsg(chan, 'Q:)')
                elif msg == 'h' and functions.lucky() : self.sendmsg(chan, 'h')
                elif msg == '@help':
                    help_data = debug.help()
                    for item in help_data.split('\n'):
                        self.notice(nick, item)
            elif msg.startswith('.'):
                cmd  = msg.split()[0].replace('.', '', 1)
                args = msg.replace(msg.split()[0], '', 1)[1:]
                if time.time() - config.last_time < 3:
                    self.sendmsg(chan, color('Slow down nerd!', red))
                elif not args:
                    if cmd == 'btc':
                        self.sendmsg(chan, '%s - %s' % (color('BTC', orange), cryptocurrency.btc()))
                    elif cmd == 'date':
                        self.sendmsg(chan, functions.date())
                    elif cmd == 'dickserv':
                        self.sendmsg(chan, bold + 'DickServ IRC Bot - Developed by AK in Python 3.5 - https://github.com/acidvegas/dickserv/')
                    elif cmd == 'fml':
                        self.sendmsg(chan, '%s - %s' % (color('FML', black, cyan), fml.lookup()))
                    elif cmd == 'ltc':
                        self.sendmsg(chan, '%s - %s' % (color('LTC', grey), cryptocurrency.ltc()))
                    elif cmd == 'talent':
                        if functions.random_int(1,1000) == 420:
                            self.sendmsg(chan, color('HOLY FUCKING TALENT PANTS !!! ANAL TALENT ACQUIRED!!! XDD XDD', red, blue))
                        else:
                            self.sendmsg(chan, color('(^)', 'random'))
                    elif cmd == 'todo':
                        self.error(chan, 'Not done...') #todo.read(chan)
                    elif cmd == 'uptime':
                        self.sendmsg(chan, functions.uptime())
                else:
                    if cmd == 'ascii':
                        lines = ascii.read(args)
                        if lines:
                            if len(lines) > 50 and chan != '#scroll':
                                self.error(chan, 'File is too big. Take it to #scroll bo.')
                            else:
                                for line in lines:
                                    self.sendmsg(chan, line)
                        else:
                            self.error(chan, 'Invalid file name. ' + color('(Use ".ascii list" for a list of valid file names.)', grey))
                    elif cmd == 'define':
                        definition = dictionary.scrabble(args)
                        if definition : self.sendmsg(chan, '%s - %s: %s' % (color('Definition', white, blue), args.lower(), definition))
                        else          : self.error(chan, 'No results found.')
                    elif cmd == 'g':
                        self.error(chan, 'Not done...') #google.search(chan, args)
                    elif cmd == 'imdb':
                        api = imdb.search(args)
                        if api:
                            self.sendmsg(chan, '%sTitle       :%s %s' % (bold, reset, color('%s %s %s' % (api['Title'], api['Rated'], api['Year']), grey)))
                            self.sendmsg(chan, '%sLink        :%s %s' % (bold, reset, color('http://imdb.com/title/' +  api['imdbID'], grey)))
                            self.sendmsg(chan, '%sGenre       :%s %s' % (bold, reset, color(api['Genre'], grey)))
                            self.sendmsg(chan, '%sRating      :%s %s' % (bold, reset, color(api['imdbRating'], grey)))
                            prefix = bold + 'Description :' + reset
                            for line in re.findall(r'.{1,60}(?:\s+|$)', api['Plot']):
                                self.sendmsg(chan, '%s %s' % (prefix, color(line, grey)))
                                prefix = '             '
                        else:
                            self.error(chan, 'No results found.')
                    elif cmd == 'isup':
                        self.sendmsg(chan, '%s is %s' % (args, isup.check(args)))
                    elif cmd == 'reddit':
                        api  = reddit.read(args)
                        if api:
                            data = list(api.keys())
                            for i in data:
                                count = str(data.index(i)+1)
                                self.sendmsg(chan, '%s %s %s%s%s%s%s' % (color('[' + str(count) + ']', pink), functions.trim(i, 70), color('[%s|' % str(api[i]['score']), white), color('+' + str(api[i]['ups']), green), color('/', white), color('-' + str(api[i]['downs']), red), color(']', white)))
                                self.sendmsg(chan, ' - ' + color(api[i]['url'], grey))
                        else:
                            self.error(chan, 'No results found.')
                    elif cmd == 'todo' and args.split()[0] == 'add':
                        self.error(chan, 'Not done...') #todo.add(chan, nick, args)
                    elif cmd == 'todo' and args.split()[0] == 'del':
                        self.error(chan, 'Not done...') #todo.delete(chan, nick, args)
                    elif cmd == 'tpb':
                        api  = tpb.search(args)
                        if api:
                            data = list(api.keys())
                            for i in data:
                                count = str(data.index(i)+1)
                                self.sendmsg(chan, '%s %s %s%s%s%s%s' % (color('[' + str(count) + ']', pink), i, color('[', white), color(api[i]['seeders'], green), color('|', white), color(api[i]['leechers'], red), color(']', white)))
                                self.sendmsg(chan, ' -  %s' % color(api[i]['url'], grey))
                        else:
                            self.error(chan, 'No results found.')
                    elif cmd == 'ud':
                        definition = dictionary.urban(args)
                        if definition : self.sendmsg(chan, '%s%s - %s: %s' % (color('urban', white, blue), color('DICTIONARY', yellow, black), args, definition))
                        else          : self.error(chan, 'No results found.')
                    elif cmd == 'wolfram':
                        results = wolfram.ask(args)
                        if results : self.sendmsg(chan, '%s%s - %s' % (color('Wolfram', red), color('Alpha', orange), results))
                        else       : self.error(chan, 'No results found.')
                    elif cmd == 'yt':
                        api  = youtube.search(args)
                        data = list(api.keys())
                        for i in data:
                            count = str(data.index(i)+1)
                            self.sendmsg(chan, '%s %s' % (color('[' + str(count) + ']', pink), functions.trim(i, 70)))
                            self.sendmsg(chan, ' - ' + color(api[i], grey))            
                config.last_time = time.time()
        except Exception as ex:
            self.error(chan, 'Command threw an exception.', ex)
            
    def event_part(self, nick, chan, reason):
        self.sendmsg(chan, '%s %s%s' % (color('BYE', 'random'), bold, nick.upper()))

    def event_private(self, nick, host, msg):
        if '\001' in msg : pass

    def event_quit(self, nick, reason):
        self.sendmsg(self.channel, '%s %s%s' % (color('BYE', 'random'), bold, nick.upper()))

    def event_url(self, chan, url):
        try:
            if youtube.check(url):
                title = youtube.title(url)
                self.sendmsg(chan, '%s%s %s%s' % (color('You', black, white), color('Tube', white, red), bold, title))
            else:
                url_type = httplib.get_type(url)
                if url_type == 'text/html':
                    title = httplib.get_title(url)
                    self.sendmsg(chan, '[%s] %s' % (color(url_type, pink), title))
                else:
                    file_name = httplib.get_file(url)
                    if file_name:
                        file_size = httplib.get_size(url)
                        self.sendmsg(chan, '[%s] %s [%s]' % (color(url_type, pink), file_name, color(file_size, blue)))

    def handle_events(self, data):
        args = data.split()
        if   args[0] == 'PING' : self.raw('PONG ' + args[1][1:])
        elif args[1] == '001'  : self.event_connect()
        elif args[1] == '433'  :
            self.nickname = self.nickname + '_'
            self.nick(self.nickname)
        elif args[1] in ('JOIN', 'KICK', 'PART', 'PRIVMSG', 'QUIT'):
            name = args[0].split('!')[0][1:]
            user = args[0].split('@')[0].split('!')[1]
            host = args[0].split('@')[1]
            if name != self.nickname:
                if args[1] == 'JOIN':
                    chan = args[2][1:]
                    self.event_join(name, chan)
                elif args[1] == 'KICK':
                    chan   = args[2]
                    kicked = args[3]
                    reason = data.split(kicked + ' :')[1]
                    self.event_kick(name, chan, kicked, reason)
                elif args[1] == 'PART':
                    chan   = args[2]
                    reason = data.split(chan + ' :')[1]
                    self.event_part(name, chan, reason)
                elif args[1] == 'PRIVMSG':
                    host = args[0].split('!')[1].split('@')[1]
                    chan = args[2]
                    msg  = data.split(args[1] + ' ' + chan + ' :')[1]
                    if chan == self.nickname:
                        self.event_private(name, host, msg)
                    else:
                        self.event_message(name, host, chan, msg)
                elif args[1] == 'QUIT':
                    reason = data.split('QUIT :')[1]
                    self.event_quit(name, reason)

    def identify(self, username, password):
        self.sendmsg('nickserv', 'identify %s %s' % (username, password))

    def join(self, chan, key=None):
        if key : self.raw('JOIN %s %s' % (chan, key))
        else   : self.raw('JOIN ' + chan)
        self.sendmsg(chan, 'Hello, I am the %s, type %s for a list of commands.' % (color('DickServ', pink), color('@help', white)))

    def listen(self):
        while True:
            try:
                data = self.sock.recv(1024)
                for line in data.split(b'\r\n'):
                    if line:
                        try    : line = line.decode('utf-8')
                        except : pass
                        debug.irc(line)
                        if len(line.split()) >= 2:
                            self.handle_events(line)
                if b'Closing Link' in data and bytes(self.nickname, 'utf-8') in data : break
            except Exception as ex:
                debug.error('Unexpected error occured.', ex)
                break
        self.event_disconnect()

    def mode(self, target, mode):
        self.raw('MODE %s %s' % (target, mode))

    def nick(self, nick):
        self.raw('NICK ' + nick)
        
    def notice(self, target, msg):
        self.raw('NOTICE %s :%s' % (target, msg))
        
    def oper(self, nick, password):
        self.raw('OPER %s %s' % (nick, password))

    def quit(self, msg=None):
        if msg : self.raw('QUIT :' + msg)
        else   : self.raw('QUIT')
		
    def raw(self, msg):
        self.sock.send(bytes(msg + '\r\n', 'utf-8'))
        
    def sendmsg(self, target, msg):
        self.raw('PRIVMSG %s :%s' % (target, msg))

DickServ = IRC(config.server, config.port, config.use_ssl, config.password, config.channel, config.key, config.nickname, config.username, config.realname, config.nickserv, config.operserv)
