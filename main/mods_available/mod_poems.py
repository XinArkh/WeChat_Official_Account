#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from random import choice


poems = ['苟利国家生死以，岂因祸福趋避之',
        '不须浪饮丁都护，世上英雄本无主',
        '君埋泉下泥销骨，我寄人间雪满头',
        '前尘往事断肠诗，侬为君痴君不知',
        '天地一逆旅，同悲万古尘',
        '浮云一别后，流水十年间',
        '寒鸦飞数点，流水绕孤村',

        '试试问我天气怎么样',
        '告诉我“翻译A文到B文+要翻译的内容”或直接“翻译+要翻译的内容”，我就可以帮你翻译',
        '想知道一份肯德基豪华鸡肉堡到底可以提供多少热量吗？发送“营养汉堡”给我，答案马上知道',
        '往事何处寻，发送“往事”看看回不去的那些年',
        '他说：“要有光”，于是世界变得明亮；他又说：“音乐响起来”，于是大地不再荒凉'
        ]


def sendPoem():
    return choice(poems)

