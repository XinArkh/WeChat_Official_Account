#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import werobot
from urllib.request import urlretrieve
from mods_available import *
import threading
import requests


robot = werobot.WeRoBot(token='token')


# @robot.handler
# def hello(message):
#     return 'Hello World!'

@robot.text
def textReply(message, session):
    if message.content[:2] != '往事':
        reply = msgReply(message, session)
    else:
        access_token = get_access_token()
        hisReply = History()
        hisImgPath = hisReply()
        media_id = upload_media(access_token, hisImgPath)
        reply = werobot.replies.ImageReply(message=message, media_id=media_id)
    return reply


@robot.voice
def vioceReply(message):
    reply = msgReply(message.recognition)
    return reply

@robot.image
def imgReply(message):
    picName = '/var/www/wx/pic/%s.jpg' %message.time
    urlretrieve(message.img, picName)
    faceReply = Face(picName)
    reply = faceReply()
    return reply

@robot.subscribe
def subscribeReply(message):
    return '来吧，上车！'


@robot.unsubscribe
def unsubscribeReply(message):
    message.content = '传书<系统提醒>掉粉了！\n'
    threadObj = threading.Thread(target=mailProcess, args=[message])
    threadObj.start()
    return


@robot.location 
def locReply(message):
    lat = message.location[0]
    lng = message.location[1]
    weaFunc = mod_weather.Weather(lat, lng)
    weaMsg = weaFunc()
    return weaMsg



def msgReply(message, session):    
    msg = message.content
    msgHead = msg[:2]
    reply = ''
    ########################## 天气模块 ##########################
    if msgHead == '天气':
        reply = '把你的定位发给我，我就告诉你天气信息，哼╭(╯^╰)╮'
    ########################## 翻译模块 ##########################
    elif msgHead == '翻译':
        msg = msg[2:]
        while msg[0] == ' ':
            msg = msg[1:]
        if msg[1:3] == '文到' and msg[4] == '文':
            fromLang = msg[0:2]
            toLang = msg[3:5]
            msg = msg[5:]
            while msg[0] == ' ':
                msg = msg[1:]
        else:
            fromLang = 'auto'
            toLang = 'auto'
        transReply = Translation(msg, fromLang, toLang)
        reply = transReply()
    ###################### 食物营养查询模块 ######################
    elif msgHead == '营养':
        food = msg[2:]
        while food[0] == ' ':
            food = food[1:]
        nutReply = Nutrition(food)
        reply = nutReply()
    ########################## 音乐模块 ##########################
    elif msgHead == '音乐':
        musicReply = Music()
        reply = musicReply()
    ########################## 邮件模块 ##########################
    elif msgHead == '传书':
        lastTime = session.get(message.source, 0)
        if message.time - lastTime <= 3600:
            reply = '别急，冷却时间还没过'
        else:
            threadObj = threading.Thread(target=mailProcess, args=[message])
            threadObj.start()
            session[message.source] = message.time
            reply = '邮件已成功发送'
    ########################## 测试模块 ##########################
    elif msgHead == '测试':
        reply = '''test'''
    ########################## 念诗模块 ##########################
    else:
        reply = sendPoem()
    return reply


def mailProcess(message):
    sendMailFunc = Mail(message)
    sendMailFunc()


def get_access_token():
    wxURL = 'https://api.weixin.qq.com/cgi-bin/token'
    params = {}
    params['grant_type'] = 'client_credential'
    params['appid'] = 'appid'
    params['secret'] = 'secret'
    r = requests.get(wxURL, params=params)
    return r.json()['access_token']


def upload_media(access_token, hisImgPath):
    uploadURL = 'https://api.weixin.qq.com/cgi-bin/media/upload'
    params = {}
    params['access_token'] = access_token
    params['type'] = 'image'
    files = {'media':open(hisImgPath, 'rb')}
    uploadRes = requests.post(uploadURL, data=params, files=files)
    return uploadRes.json()['media_id']


if __name__ == '__main__':
    # 让服务器监听在 0.0.0.0:5000
    robot.config['HOST'] = '0.0.0.0'
    robot.config['PORT'] = 5000
    robot.run()
