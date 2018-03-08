#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import time
from PIL import Image,ImageDraw,ImageFont
import os


class History:
    __address = '__address'


    def __init__(self):
        self.reply = ''
        self.url = 'http://www.lssdjt.com/'
        self.html = urlopen(self.url)
        self.bsObj = BeautifulSoup(self.html)


    def get_content(self):
        self.history = self.bsObj.find('div', {'class':'w730 mt5 clearfix'}).find('div', {'class':'box'})
        self.date = self.history.find('div', {'class':'hd'}).h4.b.get_text()
        # self.reply = self.reply + '**' + '<a href="%s">%s</a>' %(self.url, self.date) + '**\n'
        # 注意href=后面的链接要用双括号引住
        # 超链接方式存在未知问题，暂停使用
        self.reply = self.reply + '**' + '%s' %self.date + '**\n'
        self.events = self.history.find('div', {'class':'main'}).find('ul', {'class':'list clearfix'}).findAll('li')
        self.imgNumber = 0
        while 'rel' not in self.events[self.imgNumber].a.attrs.keys():
            self.imgNumber = self.imgNumber + 1
        self.imgURL = self.events[self.imgNumber].a.attrs['rel'][0]
        self.webImgPath = str(int(time.time())) + '.jpg'
        urlretrieve(self.imgURL, self.__address + 'tmp/' + self.webImgPath)
        self.count = 1
        for e in self.events:
            # 超链接方式存在未知问题，暂停使用
            # if e.a and 'rel' in e.a.attrs:
            #     self.reply = self.reply + e.a.em.get_text() + '\t' + \
            #     '<a href="%s">%s</a>' %(e.a['rel'][0], e.a.i.get_text())  + '\n'
            # else:
            #     self.reply = self.reply + e.find('em').get_text() + '\t' + e.find('i').get_text() + '\n'
            self.reply = self.reply + e.find('em').get_text() + '\t' + e.find('i').get_text() + '\n'
            self.count = self.count + 1
        self.reply = self.reply[:len(self.reply)-1]
        # print(self.reply)


    def draw_image(self):
        self.webImage = Image.open(self.__address + 'tmp/' + self.webImgPath)
        self.width=400 + self.webImage.size[0]
        self.height=17*self.count + 16 + self.webImage.size[1] + 60
        self.im=Image.new('RGB',(self.width, self.height), (255,255,255))
        self.im.paste(self.webImage, (int((self.width-self.webImage.size[0])/2), 16))
        self.dr=ImageDraw.Draw(self.im)
        # Windows 下
        # self.font=ImageFont.truetype(os.path.join('fonts',self.BASE_DIR+"\\fonts\\simsun.ttc"),16)
        # Linux 下
        self.font=ImageFont.truetype(os.path.join('fonts', "/var/www/wx/fonts/simsun.ttc"),16)
        self.dr.text((36,25+self.webImage.size[1]),self.reply,font=self.font,fill='#000000')
        # self.im.show()
        self.im.save(self.__address + self.webImgPath)

    def __call__(self):
        self.get_content()
        self.draw_image()
        return (self.__address + self.webImgPath)
        
        

# 测试用例
if __name__ == '__main__':
    f = History()
    f()
    print(f.reply)