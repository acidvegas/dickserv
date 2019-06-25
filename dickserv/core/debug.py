#!/usr/bin/env python
# DickServ IRC Bot - Developed by acidvegas in Python (https://acid.vegas/dickserv)
# debug.py

import ctypes
import logging
import os
import sys
import time

from logging.handlers import RotatingFileHandler

import config

def check_libs():
	if config.connection.proxy:
		try:
			import socks
		except ImportError:
			error_exit('Missing \'socks\' module! (https://pypi.python.org/pypi/PySocks)')
	try:
		import bs4
	except ImportError:
		error_exit('Missing \'bs4\' module. (https://pypi.python.org/pypi/beautifulsoup4)')
	try:
		import googleapiclient.discovery
	except ImportError:
		error_exit('Missing \'google-api-python-client\' module. (https://pypi.python.org/pypi/google-api-python-client/)')


def check_privileges():
	if check_windows():
		if ctypes.windll.shell32.IsUserAnAdmin() != 0:
			return True
		else:
			return False
	else:
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
		logging.debug(f'[!] - {msg} ({reason})')
	else:
		logging.debug('[!] - ' + msg)

def error_exit(msg):
	raise SystemExit('[!] - ' + msg)

def info():
	clear()
	logging.debug('#'*56)
	logging.debug('#{0}#'.format(''.center(54)))
	logging.debug('#{0}#'.format('DickServ IRC'.center(54)))
	logging.debug('#{0}#'.format('Developed by acidvegas in Python'.center(54)))
	logging.debug('#{0}#'.format('https://acid.vegas/dickserv'.center(54)))
	logging.debug('#{0}#'.format(''.center(54)))
	logging.debug('#'*56)

def irc(msg):
	logging.debug('[~] - ' + msg)

def setup_logger():
	stream_handler = logging.StreamHandler(sys.stdout)
	if config.settings.log:
		log_file	 = os.path.join(os.path.join('data','logs'), 'bot.log')
		file_handler = RotatingFileHandler(log_file, maxBytes=256000, backupCount=3)
		logging.basicConfig(level=logging.NOTSET, format='%(asctime)s | %(message)s', datefmt='%I:%M:%S', handlers=(file_handler,stream_handler))
	else:
		logging.basicConfig(level=logging.NOTSET, format='%(asctime)s | %(message)s', datefmt='%I:%M:%S', handlers=(stream_handler,))