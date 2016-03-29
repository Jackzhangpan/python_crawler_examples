#! /usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'michel_feng'

from pyquery import PyQuery as pq
import requests
import json
import urllib


def process_list():
    raw_url = r'https://mm.taobao.com/json/request_top_list.htm?page='
    headers = {'user-agent': r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36'}
    for i in range(1, 1000):
        url = raw_url + str(i)
        ret = requests.get(url=url, headers=headers)
        query = pq(ret.text)
        items = query('div.list-item')
        for item in items:
            personal_info = pq(item).find('div.personal-info')
            img = personal_info.find('div.pic img').attr('src')
            detail = personal_info.find('div.pic a').attr('href')
            top = personal_info.find('p.top')
            name = top.find('a.lady-name').text()
            age = top.find('em strong').text()
            city = top.find('em').next().text()
            mm = {u'头像': img.strip('/'), u'姓名': name, u'年龄': age, u'城市': city, u'详情链接': detail.strip('/')}
            save_brief(name, json.dumps(mm))
            save_photo(name, img.strip('/'))


def save_photo(file_name, url):
    data = urllib.urlopen('http://' + url)
    fp = open(file_name + '.jpg', 'wb')
    fp.write(data.read())
    fp.close()


def save_brief(file_name, contents):
    fp = open(file_name + '.txt', 'w+')
    fp.write(contents)
    fp.close()


if __name__ == '__main__':
    process_list()
