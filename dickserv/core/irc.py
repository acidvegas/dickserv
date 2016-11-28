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
        foreground = '{0:0>2}'.format(functions.random_int(2,13))
    if background == 'random':
        background = '{0:0>2}'.format(functions.random_int(2,13))
    if background:
        return '\x03{0},{1}{2}{3}'.format(foreground, background, msg, reset)
    else:
        return '\x03{0}{1}{2}'.format(foreground, msg, reset)

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
        self.oper_passwd  = config.oper_passwd
        self.admin_host   = config.admin_host
        self.cmd_throttle = config.cmd_throttle
        self.last_time    = 0
        self.start_time   = 0
        self.sock         = None

    def connect(self):
        try:
            self.create_socket()
            self.sock.connect((self.server, self.port))
            if self.password:
                self.raw('PASS ' + self.password)
            self.raw('USER {0} 0 * :{1}'.format(self.username, self.realname))
            self.raw('NICK ' + self.nickname)
        except Exception as ex:
            debug.error('Failed to connect to IRC server.', ex)
            self.event_disconnect()
        else:
            self.listen()

    def create_socket(self):
        if self.use_ipv6:
            self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.vhost:
            self.sock.bind((self.vhost, 0))
        if self.use_ssl:
            self.sock = ssl.wrap_socket(self.sock)

    def error(self, chan, msg, reason=None):
        if reason:
            self.sendmsg(chan, '[{0}] {1} {2}'.format(color('ERROR', red), msg, color('({0})'.format(str(reason)), grey)))
        else:
            self.sendmsg(chan, '[{0}] {1}'.format(color('ERROR', red), msg))

    def event_connect(self):
        self.start_time = time.time()
        if self.nickserv:
            self.identify(self.username, self.nickserv)
        if self.oper_passwd:
            self.oper(self.username, self.oper_passwd)
        self.join(self.channel, self.key)
        self.loops()

    def event_disconnect(self):
        self.sock.close()
        time.sleep(10)
        self.connect()

    def event_join(self, chan, nick):
        if chan == self.channel:
            self.sendmsg(chan, '{0} {1}{2}'.format(color('SMELLO', 'random'), bold, nick.upper()))

    def event_kick(self, chan, kicked):
        if chan == self.channel:
            if kicked == self.nickname:
                self.join(self.channel, self.key)
            else:
                self.sendmsg(chan, '{0} {1}{2}'.format(color('BYE', 'random'), bold, kicked.upper()))

    def event_message(self, chan, nick, msg):
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
                    cmd  = msg.split()[0][1:]
                    args = msg[len(cmd)+2:]
                    if time.time() - self.last_time < self.cmd_throttle:
                        self.sendmsg(chan, color('Slow down nerd!', red))
                    else:
                        if not args:
                            if cmd == 'btc':
                                self.sendmsg(chan, '{0} - {1}'.format(color('BTC', orange), cryptocurrency.btc()))
                            elif cmd == 'date':
                                self.sendmsg(chan, functions.date())
                            elif cmd == 'dickserv':
                                self.sendmsg(chan, bold + 'DickServ IRC Bot - Developed by acidvegas in Python 3 - https://github.com/acidvegas/dickserv')
                            elif cmd == 'ltc':
                                self.sendmsg(chan, '{0} - {1}'.format(color('LTC', grey), cryptocurrency.ltc()))
                            elif cmd == 'talent':
                                self.sendmsg(chan, color('(^)', 'random'))
                            elif cmd == 'uptime':
                                self.sendmsg(chan, functions.uptime(self.start_time))
                        else:
                            if cmd == 'define':
                                definition = dictionary.define(args)
                                if definition:
                                    self.sendmsg(chan, '{0} - {1}: {2}'.format(color('Definition', white, blue), args.lower(), definition))
                                else:
                                    self.error(chan, 'No results found.')
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
                                    self.sendmsg(chan, color('{0}Title       {1}: {2}'.format(bold, reset, color('{0} {1} {2}'.format(api['Title'], '| ' + 'Rated: ' + api['Rated'], '| Released: ' + api['Year']), light_grey)), yellow, blue))
                                    self.sendmsg(chan, color('{0}Link        {1}: {2}'.format(bold, reset, color('http://imdb.com/title/' +  api['imdbID'], light_blue)), yellow, blue))
                                    self.sendmsg(chan, color('{0}Genre       {1}: {2}'.format(bold, reset, color(api['Genre'], light_grey)), yellow, blue))
                                    self.sendmsg(chan, color('{0}Rating      {1}: {2}'.format(bold, reset, color(api['imdbRating'], yellow)), yellow, blue))
                                    prefix = bold + color('Description ',yellow, blue) + reset + ':'
                                    for line in re.findall(r'.{1,60}(?:\s+|$)', api['Plot']):
                                        self.sendmsg(chan, '{0} {1}'.format(prefix, color(line, light_grey)))
                                        prefix = '             '
                                else:
                                    self.error(chan, 'No results found.')
                            elif cmd == 'isup':
                                self.sendmsg(chan, '{0} is {1}'.format(args, isup.check(args)))
                            elif cmd == 'netsplit':
                                api = netsplit.search(args)
                                if api:
                                    data = list(api.keys())
                                    for i in data:
                                        count = str(data.index(i)+1)
                                        self.sendmsg(chan, '{0} {1} {2} / {3}'.format(color('[{0}]'.format(str(count)), pink), color(i, light_blue), color('({0})'.format(api[i]['users']), grey), color(api[i]['network'], red)))
                                        self.sendmsg(chan, color(' - ' + api[i]['topic'], grey))
                                else:
                                    self.error(chan, 'No results found.')
                            elif cmd == 'r':
                                api = reddit.read(args)
                                if api:
                                    data = list(api.keys())
                                    for i in data:
                                        count = str(data.index(i)+1)
                                        self.sendmsg(chan, '{0} {1} {2}{3}{4}{5}{6}'.format(color('[{0}]'.format(str(count)), pink), functions.trim(i, 70), color('[{0}|'.format(str(api[i]['score'])), white), color('+' + str(api[i]['ups']), green), color('/', white), color('-' + str(api[i]['downs']), red), color(']', white)))
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
                                    self.sendmsg(chan, socket.gethostbyaddr(args)[0])
                                else:
                                    self.sendmsg(chan, socket.gethostbyname(httplib.clean_url(args)))
                            elif cmd == 'steam':
                                api  = steam.search(args)
                                if api:
                                    data = list(api.keys())
                                    for i in data:
                                        count = str(data.index(i)+1)
                                        self.sendmsg(chan, '{0} {1}'.format(color('[{0}]'.format(str(count)), pink), i))
                                        self.sendmsg(chan, ' - ' + color(api[i], grey))
                                else:
                                    self.error(chan, 'No results found.')
                            elif cmd == 'tpb':
                                api  = tpb.search(args)
                                if api:
                                    data = list(api.keys())
                                    for i in data:
                                        count = str(data.index(i)+1)
                                        self.sendmsg(chan, '{0} {1} {2}{3}{4}{5}{6}'.format(color('[{0}]'.format(str(count)), pink), i, color('[', white), color(api[i]['seeders'], green), color('|', white), color(api[i]['leechers'], red), color(']', white)))
                                        self.sendmsg(chan, ' - ' + color('http://thepiratebay.org' + api[i]['url'], grey))
                                else:
                                    self.error(chan, 'No results found.')
                            elif cmd == 'ud':
                                definition = dictionary.urban(args)
                                if definition : self.sendmsg(chan, '{0}{1} - {2}: {3}'.format(color('urban', white, blue), color('DICTIONARY', yellow, black), args, definition))
                                else          : self.error(chan, 'No results found.')
                            elif cmd == 'wolfram':
                                results = wolfram.ask(args)
                                if results : self.sendmsg(chan, '{0}{1} - {2}'.format(color('Wolfram', red), color('Alpha', orange), results))
                                else       : self.error(chan, 'No results found.')
                            elif cmd == 'yt':
                                api  = youtube.search(args)
                                if api:
                                    data = list(api.keys())
                                    for i in api.keys():
                                        count = str(data.index(i)+1)
                                        self.sendmsg(chan, '{0} {1}'.format(color('[{0}]'.format(str(count)), pink), functions.trim(i, 70)))
                                        self.sendmsg(chan, ' - ' + color(api[i], grey))
                                else:
                                    self.error(chan, 'No results found.')
                    self.last_time = time.time()
        except Exception as ex:
            self.error(chan, 'Command threw an exception.', ex)

    def event_nick_in_use(self):
        debug.error_exit('DickServ is already running.')

    def event_part(self, chan, nick):
        self.sendmsg(chan, '{0} {1}{2}'.format(color('BYE', 'random'), bold, nick.upper()))

    def event_url(self, chan, url):
        try:
            if youtube.check(url):
                title = youtube.title(url)
                self.sendmsg(chan, '{0}{1} {2}{3}'.format(color('You', black, white), color('Tube', white, red), bold, title))
            elif vimeo.check(url):
                title = vimeo.title(url)
                self.sendmsg(chan, '{0} {1}{2}'.format(color('vimeo', white, cyan), bold, title))
            else:
                url_type = httplib.get_type(url)
                if url_type == 'text/html':
                    title = httplib.get_title(url)
                    self.sendmsg(chan, '[{0}] {1}'.format(color(url_type, pink), title))
                else:
                    file_name = httplib.get_file(url)
                    if file_name:
                        file_size = httplib.get_size(url)
                        self.sendmsg(chan, '[{0}] {1} [{2}]'.format(color(url_type, pink), file_name, color(file_size, blue)))
        except Exception as ex:
            debug.error('Title Error', ex)

    def event_quit(self, nick):
        self.sendmsg(self.channel, '{0} {1}{2}'.format(color('BYE', 'random'), bold, nick.upper()))

    def handle_events(self, data):
        args = data.split()
        if args[0] == 'PING':
            self.raw('PONG ' + args[1][1:])
        elif args[1] == '001': # Use 002 or 003 if you run into issues.
            self.event_connect()
        elif args[1] == '433':
            self.event_nick_in_use()
        elif args[1] in ('JOIN','KICK','PART','PRIVMSG','QUIT'):
            nick = args[0].split('!')[0][1:]
            if nick != self.nickname:
                if args[1] == 'JOIN':
                    chan = args[2][1:]
                    self.event_join(chan, nick)
                elif args[1] == 'KICK':
                    chan   = args[2]
                    kicked = args[3]
                    self.event_kick(chan, kicked)
                elif args[1] == 'PART':
                    chan = args[2]
                    self.event_part(chan, nick)
                elif args[1] == 'PRIVMSG':
                    chan = args[2]
                    msg  = data.split('{0} PRIVMSG {1} :'.format(args[0], chan))[1]
                    self.event_message(chan, nick, msg)
                elif args[1] == 'QUIT':
                    self.event_quit(nick)

    def identify(self, username, password):
        self.sendmsg('nickserv', 'identify {0} {1}'.format(username, password))

    def join(self, chan, key=None):
        if key:
            self.raw('JOIN {0} {1}'.format(chan, key))
        else:
            self.raw('JOIN ' + chan)
        self.sendmsg(chan, 'Hello, I am the {0}, type {1} for a list of commands.'.format(color('DickServ', pink), color('@help', white)))

    def listen(self):
        while True:
            try:
                data = self.sock.recv(1024).decode('utf-8')
                for line in (line for line in data.split('\r\n') if line):
                    debug.irc(line)
                    if line.startswith('ERROR :Closing Link:'):
                        raise Exception('Connection has closed.')
                    elif len(line.split()) >= 2:
                        self.handle_events(line)
            except Exception as ex:
                debug.error('Unexpected error occured.', ex)
                break
        self.event_disconnect()

    def loops(self):
        reminder.loop().start()
        unreal.loop().start()

    def oper(self, username, password):
        self.raw('OPER {0} {1}'.format(username, password))

    def raw(self, msg):
        self.sock.send(bytes(msg + '\r\n', 'utf-8'))

    def sendmsg(self, target, msg):
        self.raw('PRIVMSG {0} :{1}'.format(target, msg))

DickServ = IRC()
