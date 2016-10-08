#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3
# https://github.com/acidvegas/dickserv
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
    if foreground == 'random':
        foreground = '%02d' % functions.random_int(2,13)
    if background == 'random':
        background = '%02d' % functions.random_int(2,13)
    if background:
        return '%s%s,%s%s%s' % (colour, foreground, background, msg, reset)
    else:
        return '%s%s%s%s' % (colour, foreground, msg, reset)

class IRC(object):
    def __init__(self):
        self.server       = config.server
        self.port         = config.port
        self.use_ipv6     = config.use_ipv6
        self.use_ssl      = config.use_ssl
        self.vhost        = config.vhost
        self.password     = config.password
        self.channel      = config.channel
        self.key          = config.key
        self.nickname     = config.nickname
        self.username     = config.username
        self.realname     = config.realname
        self.nickserv     = config.nickserv
        self.operserv     = config.operserv
        self.admin_host   = config.admin_host
        self.cmd_throttle = config.cmd_throttle
        self.last_time    = 0
        self.sock         = None

    def connect(self):
        try:
            self.create_socket()
            self.sock.connect((self.server, self.port))
            if self.password:
                self.raw('PASS ' + self.password)
            self.raw('USER %s 0 * :%s' % (self.username, self.realname))
            self.raw('NICK ' + self.nickname)
        except Exception as ex:
            debug.error('Failed to connect to IRC server.', ex)
            self.event_disconnect()
        else:
            self.listen()

    def create_socket(self):
        if self.use_ipv6:
            family = socket.AF_INET6
        else:
            family = socket.AF_INET
        self.sock = socket.socket(family, socket.SOCK_STREAM)
        if self.vhost:
            self.sock.bind((self.vhost, 0))
        if self.use_ssl:
            self.sock = ssl.wrap_socket(self.sock)
            
    def disconnect(self):
        if self.sock:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except:
                pass
            self.sock.close()
            self.sock = None

    def error(self, chan, msg, reason=None):
        if reason:
            self.sendmsg(chan, '[%s] %s %s' % (color('ERROR', red), msg, color('(%s)' % str(reason), grey)))
        else:
            self.sendmsg(chan, '[%s] %s' % (color('ERROR', red), msg))

    def event_connect(self):
        config.start_time = time.time()
        if self.nickserv:
            self.identify(self.username, self.nickserv)
        if self.operserv:
            self.oper(self.nickname, self.operserv)
        self.join(self.channel, self.key)
        self.join('#scroll')
        self.loops()
        
    def event_disconnect(self):
        self.disconnect()
        time.sleep(5)
        self.connect()
        
    def event_join(self, chan, nick):
        if chan == self.channel:
            self.sendmsg(chan, '%s %s%s' % (color('SMELLO', 'random'), bold, nick.upper()))

    def event_kick(self, chan, kicked):
        if chan == self.channel:
            if kicked == self.nickname:
                self.join(self.channel, self.key)
            else:
                self.sendmsg(chan, '%s %s%s' % (color('BYE', 'random'), bold, kicked.upper()))
        elif chan == '#scroll':
            if kicked == self.nickname:
                self.join('#scroll')

    def event_message(self, chan, nick, host, msg):
        try:
            if chan == self.channel:
                if not msg.startswith('.'):
                    urls = httplib.parse_urls(msg)
                    if urls:
                        if time.time() - self.last_time > self.cmd_throttle:
                            self.last_time = time.time()
                            self.event_url(chan, urls[0])
                    if 'qhat' in msg:
                        self.sendmsg(chan, 'Q:)')
                    elif msg == 'h' and functions.lucky():
                        self.sendmsg(chan, 'h')
                    elif msg == '@help':
                        self.sendmsg(chan, 'https://github.com/acidvegas/dickserv/blob/master/README.md#commands')
                else:
                    cmd  = msg.split()[0].replace('.', '', 1)
                    args = msg[len(cmd)+2:].split()
                    if time.time() - self.last_time < self.cmd_throttle:
                        self.sendmsg(chan, color('Slow down nerd!', red))
                    else:
                        if not args:
                            if cmd == 'btc':
                                self.sendmsg(chan, '%s - %s' % (color('BTC', orange), cryptocurrency.btc()))
                            elif cmd == 'date':
                                self.sendmsg(chan, functions.date())
                            elif cmd == 'dickserv':
                                self.sendmsg(chan, bold + 'DickServ IRC Bot - Developed by acidvegas in Python 3 - https://github.com/acidvegas/dickserv')
                            elif cmd == 'ltc':
                                self.sendmsg(chan, '%s - %s' % (color('LTC', grey), cryptocurrency.ltc()))
                            elif cmd == 'talent':
                                self.sendmsg(chan, color('(^)', 'random'))
                            elif cmd == 'uptime':
                                self.sendmsg(chan, functions.uptime())
                        else:
                            if cmd == 'ascii':
                                split = args.split()
                                if split[0] == 'delete' and len(split)== 2 and host == self.admin_host:
                                    ascii.delete(split[1])
                                    self.sendmsg(chan, 'File deleted.')
                                elif split[0] == 'rename' and len(split) == 3 and host == self.admin_host:
                                    ascii.rename(split[1], split[2])
                                    self.sendmsg(chan, 'File renamed.')
                                else:
                                    lines = ascii.read(args)
                                    if lines:
                                        if len(lines) > 50:
                                            self.error(chan, 'File is too big.', 'Take it to %s' % color('#scroll', light_blue))
                                        else:
                                            for line in lines:
                                                self.sendmsg(chan, line)
                                    else:
                                        self.error(chan, 'Invalid file name.', 'Use ".ascii list" for a list of valid file names.')
                            elif cmd == 'define':
                                definition = dictionary.scrabble(args)
                                if definition:
                                    self.sendmsg(chan, '%s - %s: %s' % (color('Definition', white, blue), args.lower(), definition))
                                else:
                                    self.error(chan, 'No results found.')
                            elif cmd == 'filter':
                                if args == 'enable':
                                    self.mode(self.channel, '+G')
                                elif args == 'disable':
                                    self.mode(self.channel, '-G')
                            elif cmd == 'flood' and host == self.admin_host:
                                if args == 'enable':
                                    self.mode(self.channel, '-f [30m,10t]:10')
                                elif args == 'disable':
                                    self.mode(self.channel, '+f [10t,30m]:10')
                            elif cmd == 'geoip':
                                if functions.check_ip(args):
                                    results = geoip.lookup(args)
                                    if results:
                                        self.sendmsg(chan, results)
                                    else:
                                        self.error(chan, 'No information found.')
                                else:
                                    self.error(chan, 'Invalid IP address.')
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
                            elif cmd == 'r':
                                api = reddit.read(args)
                                if api:
                                    data = list(api.keys())
                                    for i in data:
                                        count = str(data.index(i)+1)
                                        self.sendmsg(chan, '%s %s %s%s%s%s%s' % (color('[' + str(count) + ']', pink), functions.trim(i, 70), color('[%s|' % str(api[i]['score']), white), color('+' + str(api[i]['ups']), green), color('/', white), color('-' + str(api[i]['downs']), red), color(']', white)))
                                        self.sendmsg(chan, ' - ' + color(api[i]['url'], grey))
                                else:
                                    self.error(chan, 'No results found.')
                            elif cmd == 'remind':
                                if len(args.split()) >= 2:
                                    duration = args.split()[0][:-1]
                                    type     = args.split()[0][-1:]
                                    data     = args[len(args.split()[0])+1:]
                                    if duration.isdigit():
                                        duration = int(duration)
                                        if duration > 0:
                                            if (type == 'm' and (duration <= 43200 or duration >= 20)) or (type == 'h' and duration <= 720) or (type == 'd' and duration <= 30):
                                                if len(config.reminders) < 20:
                                                    reminder.add(nick, duration, type, data)
                                                    self.sendmsg(chan, 'Added new reminder to the database!')
                                                else:
                                                    self.error(chan, 'Too many reminders.', 'The max is 20.')
                                            else:
                                                self.error(chan, 'Invalid arguments.', 'Duration is too high or low for the given type.')
                                    else:
                                        self.error(chan, 'Invalid arguments.')
                                else:
                                    self.error(chan, 'Missing arguments.')
                            elif cmd == 'resolve':
                                if functions.check_ip(args):
                                    self.sendmsg(chan, resolve.host(args))
                                else:
                                    self.sendmsg(chan, resolve.url(httplib.clean_url(args)))
                            elif cmd == 'steam':
                                api  = steam.search(args)
                                if api:
                                    data = list(api.keys())
                                    for i in data:
                                        count = str(data.index(i)+1)
                                        self.sendmsg(chan, '%s %s' % (color('[' + str(count) + ']', pink), i))
                                        self.sendmsg(chan, ' - ' + color(api[i], grey))
                                else:
                                    self.error(chan, 'No results found.')
                            elif cmd == 'tpb':
                                api  = tpb.search(args)
                                if api:
                                    data = list(api.keys())
                                    for i in data:
                                        count = str(data.index(i)+1)
                                        self.sendmsg(chan, '%s %s %s%s%s%s%s' % (color('[' + str(count) + ']', pink), i, color('[', white), color(api[i]['seeders'], green), color('|', white), color(api[i]['leechers'], red), color(']', white)))
                                        self.sendmsg(chan, ' - ' + color(api[i]['url'], grey))
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
                                if api:
                                    data = list(api.keys())
                                    for i in api.keys():
                                        count = str(data.index(i)+1)
                                        self.sendmsg(chan, '%s %s' % (color('[' + str(count) + ']', pink), functions.trim(i, 70)))
                                        self.sendmsg(chan, ' - ' + color(api[i], grey))
                                else:
                                    self.error(chan, 'No results found.')
                        self.last_time = time.time()
            if chan == '#scroll':
                cmd  = msg.split()[0].replace('.', '', 1)
                args = msg.replace(msg.split()[0], '', 1)[1:]
                if time.time() - self.last_time < self.cmd_throttle:
                    self.sendmsg(chan, color('Slow down nerd!', red))
                elif cmd == 'ascii':
                    split = args.split()
                    if split[0] == 'delete' and len(split)== 2 and host == self.admin_host:
                        ascii.delete(split[1])
                        self.sendmsg(chan, 'File deleted.')
                    elif split[0] == 'rename' and len(split) == 3 and host == self.admin_host:
                        ascii.rename(split[1], split[2])
                        self.sendmsg(chan, 'File renamed.')
                    else:
                        lines = ascii.read(args)
                        if lines:
                            for line in lines:
                                self.sendmsg(chan, line)
                        else:
                            self.error(chan, 'Invalid file name.', 'Use ".ascii list" for a list of valid file names.')
                    self.last_time = time.time()
        except Exception as ex:
            self.error(chan, 'Command threw an exception.', ex)

    def event_nick_in_use(self):
        debug.error_exit('DickServ is already running.')
            
    def event_part(self, chan, nick):
        self.sendmsg(chan, '%s %s%s' % (color('BYE', 'random'), bold, nick.upper()))

    def event_url(self, chan, url):
        try:
            if youtube.check(url):
                title = youtube.title(url)
                self.sendmsg(chan, '%s%s %s%s' % (color('You', black, white), color('Tube', white, red), bold, title))
            elif vimeo.check(url):
                title = vimeo.title(url)
                self.sendmsg(chan, '%s %s%s' % (color('vimeo', white, cyan), bold, title))
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
        except Exception as ex:
            debug.error('Title Error', ex)

    def handle_events(self, data):
        args = data.split()
        if args[0] == 'PING':
            self.raw('PONG ' + args[1][1:])
        elif args[1] == '001': # Use 002 or 003 if you run into issues.
            self.event_connect()
        elif args[1] == '433':
            self.event_nick_in_use()
        elif args[1] in ('JOIN','KICK','PART','PRIVMSG'):
            name = args[0].split('!')[0][1:]
            if name != self.nickname:
                chan = args[2]
                if self.channel in chan or '#scroll' in chan:
                    if args[1] == 'JOIN':
                        self.event_join(chan[1:], name)
                    elif args[1] == 'KICK':
                        kicked = args[3]
                        self.event_kick(chan, kicked)
                    elif args[1] == 'PART':
                        self.event_part(chan, name)
                    elif args[1] == 'PRIVMSG':
                        msg  = data.split(args[1] + ' ' + chan + ' :')[1]
                        host = args[0].split('!')[1].split('@')[1]
                        self.event_message(chan, name, host, msg)
                else:
                    self.part(chan, 'smell ya later')

    def identify(self, username, password):
        self.sendmsg('nickserv', 'identify %s %s' % (username, password))

    def join(self, chan, key=None):
        if key:
            self.raw('JOIN %s %s' % (chan, key))
        else:
            self.raw('JOIN ' + chan)
        if self.operserv:
            self.mode(chan, '+q ' + self.nickname)
        self.sendmsg(chan, 'Hello, I am the %s, type %s for a list of commands.' % (color('DickServ', pink), color('@help', white)))

    def listen(self):
        while True:
            try:
                data = self.sock.recv(1024)
                for line in data.split(b'\r\n'):
                    if line:
                        try:
                            line = line.decode('utf-8')
                        except:
                            pass
                        debug.irc(line)
                        if len(line.split()) >= 2:
                            self.handle_events(line)
                if b'Closing Link' in data and bytes(self.nickname, 'utf-8') in data:
                    break
            except Exception as ex:
                debug.error('Unexpected error occured.', ex)
                break
        self.event_disconnect()

    def loops(self):
        reminder.loop().start()
        unreal.loop().start()

    def mode(self, target, mode):
        self.raw('MODE %s %s' % (target, mode))

    def notice(self, target, msg):
        self.raw('NOTICE %s :%s' % (target, msg))

    def oper(self, username, password):
        self.raw('OPER %s %s' % (username, password))

    def part(self, chan,  msg):
        self.raw('PART %s %s' % (chan, msg))
		
    def raw(self, msg):
        self.sock.send(bytes(msg + '\r\n', 'utf-8'))
        
    def sendmsg(self, target, msg):
        self.raw('PRIVMSG %s :%s' % (target, msg))

DickServ = IRC()
