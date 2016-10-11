#!/usr/bin/env python
# DickServ IRC Service Bot
# Developed by acidvegas in Python 3
# https://github.com/acidvegas/dickserv/
# steam.py

import httplib

from bs4 import BeautifulSoup

def search(query):
    api   = httplib.get_source('https://store.steampowered.com/search/?term=' + query)
    soup  = BeautifulSoup(api)
    games = soup.find_all('span', {'class':'title'})
    games = [game.text for game in games]
    urls  = soup.find_all('a', {'class':'search_result_row ds_collapse_flag'})
    urls  = ['https://store.steampowered.com/app/' + url['data-ds-appid'] for url in urls]
    if games and urls:
        if len(games) > 10:
            games = games[:10]
        if len(urls) > 10:
            urls = urls[:10]
        return dict(zip(games, urls))
    else:
        return False
