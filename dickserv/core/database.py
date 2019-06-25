#!/usr/bin/env python
# DickServ IRC Bot - Developed by acidvegas in Python (https://acid.vegas/dickserv)
# database.py

import os
import sqlite3

# Globals
db  = sqlite3.connect(os.path.join('data', 'bot.db'), check_same_thread=False)
sql = db.cursor()

def check():
	tables = sql.execute('SELECT name FROM sqlite_master WHERE type=\'table\'').fetchall()
	if not len(tables):
		sql.execute('CREATE TABLE IGNORE (IDENT TEXT NOT NULL);')
		sql.execute('CREATE TABLE SETTINGS (SETTING TEXT NOT NULL, VALUE INTEGER NOT NULL);')
		sql.execute('INSERT INTO SETTINGS (SETTING,VALUE) VALUES (?, ?)', ('max_results',  5))
		sql.execute('INSERT INTO SETTINGS (SETTING,VALUE) VALUES (?, ?)', ('max_todo',   100))
		sql.execute('INSERT INTO SETTINGS (SETTING,VALUE) VALUES (?, ?)', ('max_todo_per', 5))
		sql.execute('INSERT INTO SETTINGS (SETTING,VALUE) VALUES (?, ?)', ('todo_expire',  7))
		sql.execute('CREATE TABLE TODO (DATE TEXT NOT NULL, IDENT TEXT NOT NULL, DATA TEXT NOT NULL);')
		db.commit()

class Ignore:
	def add(ident):
		sql.execute('INSERT INTO IGNORE (IDENT) VALUES (?)', (ident,))
		db.commit()

	def idents():
		return list(item[0] for item in sql.execute('SELECT IDENT FROM IGNORE ORDER BY IDENT ASC').fetchall())

	def remove(ident):
		sql.execute('DELETE FROM IGNORE WHERE IDENT=?', (ident,))
		db.commit()

	def reset():
		sql.execute('DROP TABLE IGNORE')
		sql.execute('CREATE TABLE IGNORE (IDENT TEXT NOT NULL);')
		db.commit()

class Settings:
	def get(setting):
		return sql.execute('SELECT VALUE FROM SETTINGS WHERE SETTING=?', (setting,)).fetchone()[0]

	def read():
		return sql.execute('SELECT SETTING,VALUE FROM SETTINGS ORDER BY SETTING ASC').fetchall()

	def settings():
		return list(item[0] for item in sql.execute('SELECT SETTING FROM SETTINGS').fetchall())

	def update(setting, value):
		sql.execute('UPDATE SETTINGS SET VALUE=? WHERE SETTING=?', (value, setting))
		db.commit()

class Todo:
	def add(date, ident, data):
		sql.execute('INSERT INTO TODO (DATE,IDENT,DATA) VALUES (?,?,?)', (date, ident, data))
		db.commit()

	def expire_check():
		todos = set(list(item[0] for item in sql.execute('SELECT DATE FROM TODO').fetchall()))
		for date in todos:
			if functions.timespan(date) > Settings.get('todo_expire'):
				sql.execute('DELETE FROM TODO WHERE DATE=?', (date,))
				db.commit()

	def idents():
		return list(item[0] for item in sql.execute('SELECT IDENT FROM TODO').fetchall())

	def read(ident=None):
		if ident:
			return list(item[0] for item in sql.execute('SELECT DATA FROM TODO WHERE IDENT=?', (ident,)).fetchall())
		else:
			return sql.execute('SELECT DATE,IDENT,DATA FROM TODO ORDER BY DATE ASC, IDENT ASC, DATA ASC').fetchall()

	def remove(ident, data):
		sql.execute('DELETE FROM TODO WHERE IDENT=? AND DATA=?', (ident, data))
		db.commit()

	def reset():
		sql.execute('DROP TABLE TODO')
		sql.execute('CREATE TABLE TODO (DATE TEXT NOT NULL, IDENT TEXT NOT NULL, DATA TEXT NOT NULL);')
		db.commit()