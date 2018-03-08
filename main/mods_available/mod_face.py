#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import requests
import json


class Face:
    __KEY = '__KEY'
    __SECRET = '__SECRET'
    URL = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    params = {}
    files = {}
    reply = ''
    ethnicity = {'Asian':'亚洲人', 'White':'白人', 'Black':'黑人'}


    def __init__(self, link):
        self.link = link
        self.params['api_key'] = self.__KEY
        self.params['api_secret'] = self.__SECRET
        self.params['return_attributes'] = 'gender,age,emotion,ethnicity,beauty,skinstatus'
        self.files = {'image_file':open(self.link, 'rb')}

    def getFace(self):
        try:
            self.res = requests.post(self.URL, data=self.params, files=self.files).content.decode('UTF-8')
        # print(self.res.content)
        except Exception as e:
            print('Exception in mod_face.py-->class Face-->getFace\n%s') %e
            return
        # print(self.res)
        self.resJson = json.loads(self.res)
        # print(len(self.resJson['faces']))
        

    def getReply(self):
        if len(self.resJson['faces']) == 1:
            # print('\n\n', self.resJson['faces'][0]['attributes']['emotion']['anger'], '\n\n')
            self.face = self.resJson['faces'][0]['attributes']
            self.reply = self.reply + '**概况**\n'
            self.reply = self.reply + '性别:%s\n年龄:%s\n' %(self.face['gender']['value'], self.face['age']['value'])
            self.reply = self.reply + '人种:%s\n' %self.ethnicity[self.face['ethnicity']['value']]
            self.reply = self.reply + '**颜值**\n'
            self.reply = self.reply + '男性视角:%s分\n女性视角:%s分\n' %(self.face['beauty']['male_score'], \
                        self.face['beauty']['female_score'])
            self.reply = self.reply + '**情绪**\n'
            self.reply = self.reply + '幸福:%s%%\n淡然:%s%%\n忧郁:%s%%\n惊讶:%s%%\n恐惧:%s%%\n厌恶:%s%%\n愤怒:%s%%\n' \
                            %(self.face['emotion']['happiness'], self.face['emotion']['neutral'], \
                            self.face['emotion']['sadness'], self.face['emotion']['surprise'], self.face['emotion']['fear'], \
                            self.face['emotion']['disgust'], self.face['emotion']['anger'])
            self.reply = self.reply + '**气质**\n'
            self.reply = self.reply + '健康度:%s%%\n色斑:%s%%\n青春痘:%s%%\n黑眼圈:%s%%\n' \
                            %(self.face['skinstatus']['health'], self.face['skinstatus']['stain'], \
                            self.face['skinstatus']['acne'], self.face['skinstatus']['dark_circle'])
        else:
            count = 1
            for f in self.resJson['faces']:
                if count == 1:
                    self.reply = self.reply + '***顺序第%s位***\n' %count
                else:
                    self.reply = self.reply + '\n***顺序第%s位***\n' %count
                self.face = self.resJson['faces'][0]['attributes']
                self.reply = self.reply + '**概况**\n'
                self.reply = self.reply + '性别:%s\n年龄:%s\n' %(self.face['gender']['value'], self.face['age']['value'])
                self.reply = self.reply + '人种:%s\n' %self.ethnicity[self.face['ethnicity']['value']]
                self.reply = self.reply + '**颜值**\n'
                self.reply = self.reply + '男性视角:%s分\n女性视角:%s分\n' %(self.face['beauty']['male_score'], \
                            self.face['beauty']['female_score'])
                self.reply = self.reply + '**情绪**\n'
                self.reply = self.reply + '幸福:%s%%\n淡然:%s%%\n忧郁:%s%%\n惊讶:%s%%\n恐惧:%s%%\n厌恶:%s%%\n愤怒:%s%%\n' \
                                %(self.face['emotion']['happiness'], self.face['emotion']['neutral'], \
                                self.face['emotion']['sadness'], self.face['emotion']['surprise'], self.face['emotion']['fear'], \
                                self.face['emotion']['disgust'], self.face['emotion']['anger'])
                self.reply = self.reply + '**气质**\n'
                self.reply = self.reply + '健康度:%s%%\n色斑:%s%%\n青春痘:%s%%\n黑眼圈:%s%%\n' \
                                %(self.face['skinstatus']['health'], self.face['skinstatus']['stain'], \
                                self.face['skinstatus']['acne'], self.face['skinstatus']['dark_circle'])
                count = count + 1
        self.reply = self.reply[:len(self.reply)-1]


    def __call__(self):
        self.getFace()
        self.getReply()
        return self.reply




# 测试用例
if __name__ == '__main__':
    f = Face('../pic/test.jpg')
    print(f())