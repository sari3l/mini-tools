#!/usr/bin/env python2
# coding: utf-8
# weizx@2017-09-05 13:17:11
# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4:

'''
使用 weibo 图片 url 找出发图人 id
'''

# ref
# https://www.v2ex.com/t/388152
# https://gist.github.com/zh-h/c5adc0dc4f0b96b00040aab9b8df93e6

import sys

def str62_to_int(s):
    base = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    n = 0
    index = 0
    for i in s[::-1]:
        n += base.index(i) * 62 ** index
        index += 1
    return n

def str2int(s):
    s = s[:8]
    return str62_to_int(s) if s.startswith('00') else int(s, 16)

def find_uid(url):
    s = url.rsplit('/', 1)[-1]
    return str2int(s)

if __name__ == '__main__':
    url = sys.argv[1]
    print 'https://weibo.com/u/%s' % find_uid(url)
