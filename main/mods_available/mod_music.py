#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import os
import re
from random import choice
from urllib.parse import quote


class Music:
    __address = '__address'
    __link = '__link'


    def __init__(self):
        self.reply = []
        self.pathDir =  os.listdir(self.__address)
        # print(choice(pathDir))
        self.musicFile = choice(self.pathDir)
        # 测试
        self.musicFile = 'BEYOND - 不再犹豫.mp3'


    def wordSplit(self):
        self.tmp = re.split('-|\.', self.musicFile)
        # print(self.tmp)
        self.reply.append(self.tmp[1])
        self.reply.append(self.tmp[0])
        self.reply.append(self.__link + quote(self.musicFile))


    def __call__(self):
        self.wordSplit()
        repr(self.reply)
        return self.reply


# 测试用例
if __name__ == '__main__':
    f = Music()
    print(f())