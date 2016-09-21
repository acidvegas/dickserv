#!/usr/bin/env python
# DickServ IRC Service Bot
# Developed by acidvegas in Python 3
# https://github.com/acidvegas/dickserv
# youtube.py

import re

import httplib

def check(url):
    return re.match('^(http(s?):\/\/)?(www\.)?youtu(be)?\.([a-z])+\/(watch(.*?)(\?|\&)v=)?(.*?)(&(.)*)?$', url)

def title(url):
    video_id = check(url).group(9)
    api      = 'https://www.googleapis.com/youtube/v3/videos?key=AIzaSyC6lTRPIY-6P0zcpMggqY9mVEC2ZvXUcas&part=snippet,contentDetails,statistics&id=%s' % video_id
    data     = httplib.get_json(api)
    return data['items'][0]['snippet']['title']

def search(query):
    api    = 'https://www.googleapis.com/youtube/v3/search?part=snippet&key=AIzaSyC6lTRPIY-6P0zcpMggqY9mVEC2ZvXUcas&q=%s&maxResults=10&&fields=items' % httplib.data_quote(query)
    data   = httplib.get_json(api)
    results = {}
    for item in data['items']:
        title   = item['snippet']['title']
        content = item['id']['kind']
        if   content == 'youtube#channel'  : url = 'https://www.youtube.com/channel/' + item['id']['channelId']
        elif content == 'youtube#playlist' : url = 'https://www.youtube.com/playlist?list=' + item['id']['playlistId']
        elif content == 'youtube#video'    : url = 'https://www.youtube.com/watch?v=' + item['id']['videoId']
        results[title] = url
    return results
