#!usr/bin/env python
# -*- coding: utf-8 -*-
import cookielib
import os
import re
import json
import socket
import time
import random
import sys
import urllib2

from BeautifulSoup import BeautifulSoup
from pip._vendor import requests


def getVideoInfo(url):
    timeout = 200
    socket.setdefaulttimeout(timeout)
    sleep_download_time = 2
    time.sleep(sleep_download_time)

    headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Proxy-Connection':'keep-alive',
    'Host':'www.85porn.net',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }




    # request = urllib2.Request(url,headers=headers)
    request = urllib2.Request(url)
    # webContent = urllib2.urlopen(request)
    webContent = requests.get(url)
    data = webContent.read()
    webContent.close()
    # 利用BeautifulSoup读取视频列表网页数据
    soup = BeautifulSoup(data)

    #获取videl url
    videoSource = soup.findAll('source')
    videoUrl = ''
    for singleRes in videoSource:
        videoUrl =  singleRes['src']  # 依次取出不同匹配内容

        #获取video title
    title = soup.findAll('h4',{'class':'visible-xs big-title-truncate m-t-0'})[0].string
    return videoUrl,title



def getTrueLink(videoid):
    data = urllib2.urlopen('http://v.youku.com/player/getPlayList/VideoIDS/' + videoid)
    info = json.loads(data.read().decode('utf8'))

    segs = info['data'][0]['segs']
    types = segs.keys()

    seed = info['data'][0]['seed']
    source = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/\\:._-1234567890")
    mixed = ''
    while source:
        seed = (seed * 211 + 30031) & 0xFFFF
        index = seed * len(source) >> 16
        c = source.pop(index)
        mixed += c

    ids = info['data'][0]['streamfileids']['flv'].split('*')[:-1]
    vid = ''.join(mixed[int(i)] for i in ids)

    sid = '%s%s%s' % (int(time.time() * 1000), random.randint(1000, 1999), random.randint(1000, 9999))

    urls = []
    for s in segs['flv']:
        no = '%02x' % int(s['no'])
        url = 'http://f.youku.com/player/getFlvPath/sid/%s_%s/st/flv/fileid/%s%s%s?K=%s&ts=%s' % (
        sid, no, vid[:8], no.upper(), vid[10:], s['k'], s['seconds'])
        urls.append(url)
    return urls


def down2file(url, title):

    try:
        f = open(title, 'wb')

        req = urllib2.Request(url)
        data = urllib2.urlopen(req).read()

        # size = len(data)/1024/1024
        # if(size>10): #自动跳过大于10M的视频
        #     return

        f.write(data)
        f.close()
        print('download ' + title + ' OK!')
    except:
        print('download ' + title + ' Failed!')
        pass


def youkuDown(link):
    try:
        videoUrl,title = getVideoInfo(link)
        dir = 'G:/pydownload/'+title + '.mp4'
        if os.path.exists(dir):
            return
        down2file(videoUrl, dir+title + '.mp4')
    except urllib2.URLError, e:
        print e
        print link + ' download Failed !'
        pass


if __name__ == '__main__':
    title = requests.get('http://www.85porn.net/video/10243')
    print title
    # youkuDown('http://www.85porn.net/video/32')
    # i = 65
    # while(i):
    #    youkuDown('http://www.85porn.net/video/'+str(i))
    #    i = i+1