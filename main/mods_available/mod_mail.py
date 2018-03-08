#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


class Mail:
    __fromAddr = '__fromAddr'
    __passWord = '__passWord'
    __toAddr = '__toAddr'
    __smtpServer = '__smtpServer'


    def __init__(self, message):
        self.message = message
        self.message.content = self.message.content[2:]


    def _formatAddr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))


    def __call__(self):
        msg = MIMEText('Message from user(ID:%s):\n\t%s\nTime:%s' %(self.message.source, \
                        self.message.content, self.message.time), 'plain', 'utf-8')
        # print(type(msg))
        msg['From'] = self._formatAddr('公众号用户 <%s>' % self.__fromAddr)
        msg['To'] = self._formatAddr('管理员 <%s>' % self.__toAddr)
        msg['Subject'] = Header('公众号用户消息', 'utf-8').encode()

        server = smtplib.SMTP_SSL(self.__smtpServer, 994)
        # server.set_debuglevel(1)
        server.login(self.__fromAddr, self.__passWord)
        server.sendmail(self.__fromAddr, [self.__toAddr], msg.as_string())
        server.quit()
        # print('Mail sent.')


# 测试用例
if __name__ == '__main__':
    class Message:
        source = 'source'
        content = 'content'
        time = 1514544815  # UNIX时间戳


    message = Message()
    f = Mail(message)
    f()