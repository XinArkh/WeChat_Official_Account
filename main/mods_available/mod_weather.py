#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from urllib.request import urlopen
from urllib.parse import quote
import json


class Weather:
    __appKey = '__appKey'
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng
        self.locUrl = 'http://api.map.baidu.com/geocoder/v2/?location=' + \
            '%s,%s&output=json&pois=0&ak=%s' \
            % (self.lat, self.lng, self.__appKey)
        self.weaUrl = 'http://www.sojson.com/open/api/weather/json.shtml?city='

    def getLoc(self):
        try:
            self.res = urlopen(self.locUrl).read().decode('UTF-8')
        except HTTPError as e:
            print('HTTPError in mod_weather.py-->class Weather-->getLoc\n%s') %e
            return

        self.resJson = json.loads(self.res)
        if self.resJson.get('status') == 0:
            self.address = self.resJson.get('result').get('formatted_address')
            self.city = self.resJson.get('result').get(
                'addressComponent').get('city')
            # print(self.address, self.city)
        else:
            print('Error in mod_weather.py-->class Weather-->getLoc: %s' \
                %self.resJson.get('status'))
            return

    def getWeather(self):
        self.weatherUrl = self.weaUrl + quote(self.city)
        # print(self.weatherUrl, type(self.weatherUrl))
        try:
            self.weatherRes = urlopen(self.weatherUrl).read().decode('UTF-8')
            # print(str(self.weatherRes))
        except Exception as e:
            print('Error in mod_weather.py-->class Weather-->getWeather:\n%s') %e
            return

        self.weatherJson = json.loads(self.weatherRes)
        # print(self.weatherJson)
        if self.weatherJson.get('status') == 200:
            # 当前天气状况
            self.humidity = self.weatherJson.get('data').get('shidu')
            self.temperature = self.weatherJson.get('data').get('wendu')
            self.tip = self.weatherJson.get('data').get('ganmao')
            # 昨天天气self.yesterday和未来天气self.forecast都是Python字典，包含的
            # key有date，sunrise，high，low，sunset，aqi，fx，fl，type，notice
            # 昨天天气
            self.yesterday = self.weatherJson.get('data').get('yesterday')
            # 未来五天天气（包括今天），forecast[0-4]分别是今天到未来四天的天气
            self.forecast = self.weatherJson.get('data').get('forecast')
        else:
            print('Error in mod_weather.py-->class Weather-->getWeather: %s' \
                %self.weatherJson.get('status'))
            return

    def showWeather(self):
        # 昨日天气
        msg = '**昨日(%s)天气状况**\n' %self.yesterday['date']
        msg = msg + '最高温度：%s    最低温度：%s\n' %(self.yesterday['high'][3:], self.yesterday['low'][3:])
        msg = msg + '风向：%s  风力：%s\n' %(self.yesterday['fx'], self.yesterday['fl'])
        msg = msg + '空气质量指数：%s\n' %self.yesterday['aqi']
        msg = msg + '天气状况：%s\n\n\n\n' %self.yesterday['type']
        # 未来天气
        for i in range(5)[::-1]: 
            msg = msg + '**%s天气状况**\n' %self.forecast[i]['date']
            msg = msg + '最高温度：%s    最低温度：%s\n' %(self.forecast[i]['high'][3:], self.forecast[i]['low'][3:])
            msg = msg + '风向：%s  风力：%s\n' %(self.forecast[i]['fx'], self.forecast[i]['fl'])
            msg = msg + '空气质量指数：%s\n' %self.forecast[i]['aqi']
            msg = msg + '天气状况：%s\n' %self.forecast[i]['type']
            msg = msg + '小贴士：%s\n\n' %self.forecast[i]['notice']
        # 当前天气
        msg = msg + '\n\n**【%s】当前天气状况**\n' %self.address
        msg = msg + '温度：%s℃   湿度：%s\n' %(self.temperature, self.humidity)
        if self.tip != '-':
            msg = msg + '小贴士：%s' %self.tip
        return msg

    def __call__(self):
        self.getLoc()
        self.getWeather()
        return self.showWeather()


# 测试用例
if __name__ == '__main__':
    f = Weather(30.268, 120.123)
    print(f())