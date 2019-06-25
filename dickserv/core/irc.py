#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DickServ IRC Bot - Developed by acidvegas in Python (https://acid.vegas/dickserv)
# irc.py

import socket
import time

import config
import constants
import database
import debug
import functions
import httplib

from commands import *

# Load optional modules
if config.connection.ssl:
	import ssl
if config.connection.proxy:
	import sock

def color(msg, foreground, background=None):
	if foreground == 'random':
		foreground = '{0:0>2}'.format(functions.random_int(2,13))
	if background == 'random':
		background = '{0:0>2}'.format(functions.random_int(2,13))
	if background:
		return f'\x03{foreground},{background}{msg}{constants.reset}'
	else:
		return f'\x03{foreground}{msg}{constants.reset}'

class IRC(object):
	def __init__(self):
		self.last   = 0
		self.slow	= False
		self.sock	= None
		self.start  = 0
		self.status = True

	def connect(self):
		try:
			self.create_socket()
			self.sock.connect((config.connection.server, config.connection.port))
			self.register()
		except socket.error as ex:
			debug.error('Failed to connect to IRC server.', ex)
			Events.disconnect()
		else:
			self.listen()

	def create_socket(self):
		family = socket.AF_INET6 if config.connection.ipv6 else socket.AF_INET
		if config.connection.proxy:
			proxy_server, proxy_port = config.connection.proxy.split(':')
			self.sock = socks.socksocket(family, socket.SOCK_STREAM)
			self.sock.setblocking(0)
			self.sock.settimeout(15)
			self.sock.setproxy(socks.PROXY_TYPE_SOCKS5, proxy_server, int(proxy_port))
		else:
			self.sock = socket.socket(family, socket.SOCK_STREAM)
		if config.connection.vhost:
			self.sock.bind((config.connection.vhost, 0))
		if config.connection.ssl:
			ctx = ssl.SSLContext()
			if config.cert.file:
				ctx.load_cert_chain(config.cert.file, config.cert.key, config.cert.password)
			if config.connection.ssl_verify:
				ctx.verify_mode = ssl.CERT_REQUIRED
				ctx.load_default_certs()
			else:
				ctx.check_hostname = False
				ctx.verify_mode	= ssl.CERT_NONE
			self.sock = ctx.wrap_socket(self.sock)

	def listen(self):
		while True:
			try:
				data = self.sock.recv(1024).decode('utf-8')
				for line in (line for line in data.split('\r\n') if line):
					debug.irc(line)
					if len(line.split()) >= 2:
						Events.handle(line)
			except (UnicodeDecodeError,UnicodeEncodeError):
				pass
			except Exception as ex:
				debug.error('Unexpected error occured.', ex)
				break
		Events.disconnect()

	def register(self):
		if config.login.network:
			Commands.raw('PASS ' + config.login.network)
		Commands.raw(f'USER {config.ident.username} 0 * :{config.ident.realname}')
		Commands.nick(config.ident.nickname)



class Commands:
	def action(chan, msg):
		Commands.sendmsg(chan, f'\x01ACTION {msg}\x01')

	def error(target, data, reason=None):
		if reason:
			Commands.sendmsg(target, '[{0}] {1} {2}'.format(color('!', constants.red), data, color('({0})'.format(reason), constants.grey)))
		else:
			Commands.sendmsg(target, '[{0}] {1}'.format(color('!', constants.red), data))

	def identify(nick, password):
		Commands.sendmsg('nickserv', f'identify {nick} {password}')

	def join_channel(chan, key=None):
		Commands.raw(f'JOIN {chan} {key}') if key else Commands.raw('JOIN ' + chan)

	def mode(target, mode):
		Commands.raw(f'MODE {target} {mode}')

	def nick(nick):
		Commands.raw('NICK ' + nick)

	def notice(target, msg):
		Commands.raw(f'NOTICE {target} :{msg}')

	def oper(user, password):
		Commands.raw(f'OPER {user} {password}')

	def raw(msg):
		msg = msg.replace('\r','').replace('\n','')[:450]
		DickServ.sock.send(bytes(msg + '\r\n', 'utf-8'))

	def sendmsg(target, msg):
		Commands.raw(f'PRIVMSG {target} :{msg}')



class Events:
	def connect():
		DickServ.start = time.time()
		if config.settings.modes:
			Commands.mode(config.ident.nickname, '+' + config.settings.modes)
		if config.login.nickserv:
			Commands.identify(config.ident.nickname, config.login.nickserv)
		if config.login.operator:
			Commands.oper(config.ident.username, config.login.operator)
		Commands.join_channel(config.connection.channel, config.connection.key)

	def disconnect():
		DickServ.sock.close()
		time.sleep(10)
		DickServ.connect()

	def kick(nick, chan, kicked):
		if kicked == config.ident.nickname and chan == config.connection.channel:
			time.sleep(3)
			Commands.join_channel(chan, config.connection.key)

	def message(nick, ident, chan, msg):
		try:
			if chan == config.connection.channel and (DickServ.status or ident == config.settings.admin):
				if not msg.startswith(config.settings.cmd_char):
					urls = httplib.parse_urls(msg)
					if urls:
						if time.time() - DickServ.last > 3:
							DickServ.last = time.time()
							Events.url(chan, urls[0])
					elif msg == '@dickserv':
						Commands.sendmsg(chan, constants.bold + 'DickServ IRC Bot - Developed by acidvegas in Python - https://acid.vegas/dickserv')
					elif msg == '@dickserv help':
						Commands.sendmsg(chan, 'https://git.supernets.org/acidvegas/dickserv#commands')
					elif msg == 'h' and functions.luck(4):
						Commands.sendmsg(chan, 'h')
					elif 'qhat' in msg:
						Commands.sendmsg(chan, 'Q:)')
				elif ident not in database.Ignore.idents():
					if time.time() - DickServ.last < 3 and ident != config.settings.admin:
						if not DickServ.slow:
							Commands.sendmsg(chan, color('Slow down nerd!', constants.red))
							DickServ.slow = True
					else:
						DickServ.slow = False
						args = msg.split()
						argz = msg[len(args[0])+1:]
						cmd  = args[0][1:]
						if len(args) == 1:
							if cmd == 'date':
								Commands.sendmsg(chan, functions.current_date())
							elif cmd == 'talent':
								if functions.luck(1000):
									Commands.sendmsg(chan, color(f' !!! HOLY FUCKING SHIT {nick} ACHIEVED TALENT !!! ',               'random', 'random'))
									Commands.sendmsg(chan, color(' !!! RIP DITTLE DIP DIP DIP DIP IT\'S YOUR BIRTHDAY !!! ',          'random', 'random'))
									Commands.sendmsg(chan, color(f' !!! CAN WE HAVE A GOT DAMN MOMENT OF SILENCE FOR {nick} :) !!! ', 'random', 'random'))
									Commands.sendmsg(chan, color(' !!! GOT DAMN XD THIS IS TOO CRAZY LIKE...DAMN HAHA. DAMN. !!! ',   'random', 'random'))
								else:
									Commands.sendmsg(chan, color('(^)', 'random'))
							elif cmd == 'todo':
								todos = database.Todo.read(ident)
								if todos:
									for item in todos:
										Commands.notice(nick, '[{0}] {1}'.format(color(todos.index(item)+1, constants.pink), item))
								else:
									Commands.notice(nick, 'You have no saved todos.')
							elif cmd == 'uptime':
								Commands.sendmsg(chan, functions.uptime(DickServ.start))
						elif len(args) == 2:
							if cmd == 'coin':
								api = cryptocurrency.get(args[1])
								if api:
									Commands.sendmsg(chan, '{0} {1} - ${2:,.2f}'.format(color(api['name'], constants.white), color('({0})'.format(api['symbol']), constants.grey), float(api['price_usd'])))
								else:
									Commands.error(chan, 'Invalid cryptocurrency name!')
							elif cmd == 'drug':
								api = tripsit.drug(args[1])
								if api:
									Commands.sendmsg(chan, '{0} - {1}'.format(color(api['name'], constants.yellow), api['desc']))
								else:
									Commands.error(chan, 'No results found.')
							elif cmd == 'define':
								definition = dictionary.define(args[1])
								if definition:
									Commands.sendmsg(chan, '{0} - {1}: {2}'.format(color('Definition', constants.white, constants.blue), args[1].lower(), definition))
								else:
									Commands.error(chan, 'No results found.')
							elif cmd == 'isup':
								Commands.sendmsg(chan, '{0} is {1}'.format(args[1], isup.check(args[1])))
							elif cmd == 'r':
								api = reddit.read(args[1])
								if api:
									data = list(api.keys())
									for i in data:
										count = str(data.index(i)+1)
										Commands.sendmsg(chan, '[{0}] {1} [{2}|{3}/{4}|{5}]'.format(color(count, constants.pink), functions.trim(i, 100), color(str(api[i]['score']), constants.white), color('+' + str(api[i]['ups']), constants.green), color('-' + str(api[i]['downs']), constants.red), color(api[i]['comments'], constants.white)))
										Commands.sendmsg(chan, ' - ' + color(api[i]['url'], constants.grey))
								else:
									Commands.error(chan, 'No results found.')
							elif cmd == 'w':
								if args[1].isdigit():
									api = weather.lookup(args[1])
									if api:
										Commands.sendmsg(chan, api)
									else:
										Commands.error(chan, 'No results found.')
								else:
									Commands.error(chan, 'Invalid arguments.')
						if len(args) >= 2:
							if cmd == 'g':
								api = google.search(argz, database.Settings.get('max_results'))
								if api:
									for result in api:
										count = api.index(result)+1
										Commands.sendmsg(chan, '[{0}] {1}'.format(color(count, constants.pink), result['title']))
										Commands.sendmsg(chan, ' - ' + color(result['link'], constants.grey))
								else:
									Commands.error(chan, 'No results found.')
							elif cmd == 'imdb':
								api = imdb.search(argz)
								if api:
									Commands.sendmsg(chan, '{0} {1} {2} {3}'.format(color('Title  :', constants.white), api['Title'], api['Year'], color(api['Rated'], constants.grey)))
									Commands.sendmsg(chan, '{0} {1}{2}'.format(color('Link   :', constants.white), constants.underline, color('https://imdb.com/title/' +  api['imdbID'], constants.light_blue)))
									Commands.sendmsg(chan, '{0} {1}'.format(color('Genre  :', constants.white), api['Genre']))
									if api['imdbRating'] == 'N/A':
										Commands.sendmsg(chan, '{0} {1} 0/10'.format(color('Rating :', constants.white), color('★★★★★★★★★★', constants.grey)))
									else:
										Commands.sendmsg(chan, '{0} {1}{2} {3}/10'.format(color('Rating :', constants.white), color('★'*round(float(api['imdbRating'])), constants.yellow), color('★'*(10-round(float(api['imdbRating']))), constants.grey), api['imdbRating']))
									Commands.sendmsg(chan, '{0} {1}'.format(color('Plot   :', constants.white), api['Plot']))
								else:
									Commands.error(chan, 'No results found.')
							elif cmd == 'netsplit':
								api = netsplit.search(argz)
								if api:
									data = list(api.keys())
									for i in data:
										count = str(data.index(i)+1)
										Commands.sendmsg(chan, '[{0}] {1} {2} / {3}'.format(color(count, constants.pink), color(i, constants.light_blue), color('({0})'.format(api[i]['users']), constants.grey), color(api[i]['network'], constants.red)))
										Commands.sendmsg(chan, color(' - ' + api[i]['topic'], constants.grey))
								else:
									Commands.error(chan, 'No results found.')
							elif cmd == 'todo' and len(args) >= 3:
								if len(args) >= 3 and args[1] == 'add':
									todos = database.Todo.read(ident)
									if len(todos) <= database.Settings.get('max_todo_per') and len(database.Todo.read()) <= database.Settings.get('max_todo'):
										argz = argz[4:]
										if argz not in todos:
											database.Todo.add(functions.get_date(), ident, argz)
											Commands.notice(nick, 'Todo added to database!')
										else:
											Commands.notice(nick, 'Todo already in database!')
									else:
										Commands.notice(nick, 'Maximum todos reached!')
								elif len(args) == 3 and args[1] == 'del':
									num = args[2]
									if num.isdigit():
										num   = int(num)
										todos = database.Todo.read(ident)
										if todos:
											if num <= len(todos):
												for item in todos:
													count = todos.index(item)+1
													if count == num:
														database.Todo.remove(ident, item)
														break
												Commands.notice(nick, 'Todo removed from database!')
											else:
												Commands.notice(nick, 'Invalid number.')
										else:
											Commands.notice(nick, 'No todos found.')
									else:
										Commands.notice(nick, 'Invalid number.')
								else:
									Commands.notice(nick, 'Invalid arguments.')
							elif cmd == 'tpb':
								api = tpb.search(argz, database.Settings.get('max_results'))
								if api:
									data = list(api.keys())
									for i in data:
										count = str(data.index(i)+1)
										Commands.sendmsg(chan, '[{0}] {1} [{2}/{3}]'.format(color(count, constants.pink), i, color(api[i]['seeders'], constants.green), color(api[i]['leechers'], constants.red)))
										Commands.sendmsg(chan, ' - ' + color('http://thepiratebay.org' + api[i]['url'], constants.grey))
								else:
									Commands.error(chan, 'No results found.')
							elif cmd == 'ud':
								definition = dictionary.urban(argz)
								if definition:
									Commands.sendmsg(chan, '{0}{1} - {2}: {3}'.format(color('urban', constants.white, constants.blue), color('DICTIONARY', constants.yellow, constants.black), argz, definition))
								else:
									Commands.error(chan, 'No results found.')
							elif cmd == 'wolfram':
								results = wolfram.ask(argz)
								if results:
									Commands.sendmsg(chan, '{0}{1} - {2}'.format(color('Wolfram', constants.red), color('Alpha', constants.orange), results))
								else:
									Commands.error(chan, 'No results found.')
							elif cmd == 'yt':
								api  = youtube.search(argz, database.Settings.get('max_results'))
								if api:
									data = list(api.keys())
									for i in api.keys():
										count = str(data.index(i)+1)
										Commands.sendmsg(chan, '[{0}] {1}'.format(color(count, constants.pink), functions.trim(i, 75)))
										Commands.sendmsg(chan, ' - ' + color(api[i], constants.grey))
								else:
									Commands.error(chan, 'No results found.')
						DickServ.last = time.time()
		except Exception as ex:
			Commands.error(chan, 'Command threw an exception.', ex)

	def nick_in_use():
		debug.error('DickServ is already running or nick is in use.')

	def private(nick, ident, msg):
		try:
			if ident == config.settings.admin_host:
				args = msg.split()
				cmd  = args[0][1:]
				if len(args) == 1:
					if cmd == 'config':
						settings = database.Settings.read()
						Commands.sendmsg(nick, '[{0}]'.format(color('Settings', constants.purple)))
						for setting in settings:
							Commands.sendmsg(nick, '{0} = {1}'.format(color(setting[0], constants.yellow), color(setting[1], constants.grey)))
					elif cmd == 'ignore':
						ignores = database.Ignore.idents()
						if ignores:
							Commands.sendmsg(nick, '[{0}]'.format(color('Ignore List', constants.purple)))
							for user in ignores:
								Commands.sendmsg(nick, color(user, constants.yellow))
							Commands.sendmsg(nick, '{0} {1}'.format(color('Total:', constants.light_blue), color(len(ignores), constants.grey)))
						else:
							Commands.error(nick, 'Ignore list is empty!')
					elif cmd == 'off':
						DickServ.status = False
						Commands.sendmsg(nick, color('OFF', constants.red))
					elif cmd == 'on':
						DickServ.status = True
						Commands.sendmsg(nick, color('ON', constants.green))
				elif len(args) == 2:
					if cmd == 'ignore' and args[1] == 'reset':
						database.Ignore.reset()
					elif cmd == 'todo' and args[1] == 'expire':
						database.Todo.expire_check()
					elif cmd == 'todo' and args[1] == 'reset':
						database.Todo.reset()
				elif len(args) == 3:
					if cmd == 'config':
						setting, value = args[1], args[2]
						if functions.CheckString.number(value):
							value = functions.floatint(value)
							if value >= 0:
								if setting in database.Settings.settings():
									database.Settings.update(setting, value)
									Commands.sendmsg(nick, 'Change setting for {0} to {1}.'.format(color(setting, constants.yellow), color(value, constants.grey)))
								else:
									Commands.error(nick, 'Invalid config variable.')
							else:
								Commands.error(nick, 'Value must be greater than or equal to zero.')
						else:
							Commands.error(nick, 'Value must be an integer or float.')
					elif cmd == 'ignore':
						if args[1] == 'add':
							user_ident = args[2]
							if user_ident not in database.Ignore.idents():
								database.Ignore.add(nickname, user_ident)
								Commands.sendmsg(nick, 'Ident {0} to the ignore list.'.format(color('added', constants.green)))
							else:
								Commands.error(nick, 'Ident is already on the ignore list.')
						elif cmd == 'del':
							user_ident = args[2]
							if user_ident in database.Ignore.idents():
								database.Ignore.remove(user_ident)
								Commands.sendmsg(nick, 'Ident {0} from the ignore list.'.format(color('removed', constants.red)))
							else:
								Commands.error(nick, 'Ident does not exist in the ignore list.')
		except Exception as ex:
			Commands.error(nick, 'Command threw an exception.', ex)

	def url(chan, url):
		try:
			if imdb.check(url):
				id  = imdb.check(url)
				api = imdb.search(id)
				if api:
					Commands.sendmsg(chan, '{0} {1} {2} {3}'.format(color('Title  :', constants.white), api['Title'], api['Year'], color(api['Rated'], constants.grey)))
					Commands.sendmsg(chan, '{0} {1}{2}'.format(color('Link   :', constants.white), constants.underline, color('https://imdb.com/title/' +  api['imdbID'], constants.light_blue)))
					Commands.sendmsg(chan, '{0} {1}'.format(color('Genre  :', constants.white), api['Genre']))
					if api['imdbRating'] == 'N/A':
						Commands.sendmsg(chan, '{0} {1} 0/10'.format(color('Rating :', constants.white), color('★★★★★★★★★★', constants.grey)))
					else:
						Commands.sendmsg(chan, '{0} {1}{2} {3}/10'.format(color('Rating :', constants.white), color('★'*round(float(api['imdbRating'])), constants.yellow), color('★'*(10-round(float(api['imdbRating']))), constants.grey), api['imdbRating']))
					Commands.sendmsg(chan, '{0} {1}'.format(color('Plot   :', constants.white), api['Plot']))
			elif reddit.check(url):
				subreddit = reddit.check(url)[0]
				post_id   = reddit.check(url)[1]
				api       = reddit.post_info(subreddit, post_id)
				if api:
					Commands.sendmsg(chan, '[{0}] - {1} [{2}|{3}/{4}|{5}]'.format(color('reddit', constants.cyan), color(functions.trim(api['title'], 75), constants.white), color(api['score'], constants.white), color('+' + api['ups'], constants.green), color('-' + api['downs'], constants.red), color(api['num_comments'], constants.white)))
			elif youtube.check(url):
				api = youtube.video_info(youtube.check(url))
				if api:
					Commands.sendmsg(chan, '{0}{1} - {2} [{3}|{4}/{5}]'.format(color('You', constants.black, constants.white), color('Tube', constants.white, constants.red), functions.trim(api['title'], 75), color(api['views'], constants.white), color('+' + api['likes'], constants.green), color('-' + api['dislikes'], constants.red)))
					Commands.sendmsg(chan, color(api['description'], constants.grey))
			else:
				url_type = httplib.get_type(url)
				if url_type == 'text/html':
					title = httplib.get_title(url)
					Commands.sendmsg(chan, '[{0}] {1}'.format(color(url_type, constants.pink), color(title, constants.white)))
				else:
					file_name = httplib.get_file(url)
					if file_name:
						file_size = httplib.get_size(url)
						Commands.sendmsg(chan, '[{0}] {1} [{2}]'.format(color(url_type, constants.pink), color(file_name, constants.white), color(file_size, constants.blue)))
		except Exception as ex:
			debug.error('Title Error', ex)

	def handle(data):
		args = data.split()
		if data.startswith('ERROR :Closing Link:'):
			raise Exception('Connection has closed.')
		elif args[0] == 'PING':
			Commands.raw('PONG ' + args[1][1:])
		elif args[1] == constants.RPL_WELCOME:
			Events.connect()
		elif args[1] == constants.ERR_NICKNAMEINUSE:
			Events.nick_in_use()
		elif args[1] == constants.KICK:
			nick   = args[0].split('!')[0][1:]
			chan   = args[2]
			kicked = args[3]
			Events.kick(nick, chan, kicked)
		elif args[1] == constants.PRIVMSG:
			nick  = args[0].split('!')[0][1:]
			ident = args[0].split('!')[1]
			chan  = args[2]
			msg   = ' '.join(args[3:])[1:]
			if chan == config.ident.nickname:
				Events.private(nick, ident, msg)
			else:
				Events.message(nick, ident, chan, msg)

DickServ = IRC()
