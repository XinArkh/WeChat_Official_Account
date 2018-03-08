#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup


class Nutrition:
    def __init__(self, food):
        self.food = food
        self.mainURL = 'http://www.boohee.com'
        self.searchUrl = self.mainURL + '/food/search?keyword='
        self.searchURL = self.searchUrl + quote(self.food)


    def getHeat(self):
        try:
            # 梗概部分
            self.html = urlopen(self.searchURL)
            self.bsObj = BeautifulSoup(self.html)
            self.res = self.bsObj.find('li', {'class':'item clearfix'}).find('div', {'class':'text-box pull-left'})
            self.foodName = self.res.a.get_text()
            self.foodHeat = self.res.p.get_text()
            self.msg = '**%s**\n' %self.foodName
            # 详细信息部分
            self.detailedUrl = self.res.a.attrs['href']
            self.detailedURL = self.mainURL + self.detailedUrl
            self.dHtml = urlopen(self.detailedURL)
            self.dBsObj = BeautifulSoup(self.dHtml)
            #
            self.comment = self.dBsObj.find('body').find('div', {'id':'main'}).find('div', {'class':'content'\
                            }).find('p').get_text()[5:]
            self.msg = self.msg + self.comment
            #
            # 在服务器中写法如下：
            # self.comment = self.dBsObj.find('body').find('div', {'id':'main'}).find('div', {'class':'content'\
            #                 }).find('p').get_text()
            # self.comment =self.comment[16:len(self.comment)-8]
            # self.msg = self.msg + self.comment
            # 原因是Linux服务器和Windows系统中对待换行的编码格式不一样
            # 
            self.msg = self.msg + '每100克：\n'
            self.table = self.dBsObj.find('body').find('div', {'id':'main'}).find('div', {'class':'nutr-tag margin10'})
            self.nutritions = self.table.findAll('dl', {'class':False})
            # print(self.nutritions)
            for d in self.nutritions:
                # print(d,'\n')
                for dd in d.findAll('dd'):
                    # print(dd,'\n')
                    self.msg = self.msg + '%-9s%-s\n' %(dd.find('span', {'class':'dt'}).get_text(), dd.find('span', \
                                {'class':'dd'}).get_text())
            # print(self.msg)
        except Exception as e:
            print('Exception in mod_fruits.py-->class Fruits-->getHeat:\n%s') %e
            return
        self.msg = self.msg[:len(self.msg)-2]


    def __call__(self):
        self.getHeat()
        return self.msg


# 测试用例
if __name__ == '__main__':
    f = Nutrition('香蕉')
    print(f())