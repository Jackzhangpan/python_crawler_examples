#! /usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'michel_feng'

from pyquery import PyQuery as pq
import requests
import json
import urllib
import os

user_agent = r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36'

models = dict()


def process_list():
    raw_url = r'http://www.moko.cc/channels/post/23/'
    for i in range(1, 2):
        url = raw_url + str(i) + '.html'
        ret = requests.get(url=url, headers={'user-agent': user_agent, 'referer': url})
        query = pq(ret.text)
        items = query('ul.small-post')
        for item in items:
            cover = pq(item).find('div.cover').attr('cover-text')
            img = pq(item).find('a img').attr('src2')
            detail = 'http://www.moko.cc' + pq(item).find('a').attr('href')
            # print img
            # save_photo(cover, img.strip('/'))
            #     save_brief(name, json.dumps(mm))
            process_detail(detail)


def process_detail(url):
    ret = requests.get(url=url, headers={'user-agent': user_agent, 'referer': url})
    query = pq(ret.text)
    name = query('#workNickName').text()
    logo = query('#imgUserLogo').attr('src')
    if not os.path.exists(name):
        os.mkdir(name)
    save_photo(name + '/' + name, logo)
    if name not in models:
        models[name] = logo
        print name, logo
        items = query('p.picBox')
        for i in range(items.size()):
            item = items[i]
            img = pq(item).find('img').attr('src2')
            title = pq(item).find('img').attr('title')
            save_photo(name + '/' + name + str(i+1), img)


def save_photo(file_name, url):
    data = urllib.urlopen(url)
    fp = open(file_name + '.jpg', 'wb')
    fp.write(data.read())
    fp.close()


def save_brief(file_name, contents):
    fp = open(file_name + '.txt', 'w+')
    fp.write(contents)
    fp.close()


if __name__ == '__main__':
    process_list()
