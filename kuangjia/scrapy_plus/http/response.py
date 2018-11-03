#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 18-11-2  @Author:libo  @FileName: response.py
from lxml import etree
import json
import re

class Response:
    '''完成对响应对象的封装'''
    def __init__(self,url,body,headers,status_code,meta = None):
        '''
        初始化resposne对象
        :param url: 响应的url地址
        :param body: 响应体
        :param headers:  响应头
        :param status_code: 状态码
        :param meta: 接受request meta 值
        '''
        self.url = url
        self.headers=headers
        self.body = body
        self.status_code = status_code
        self.meta = meta


    def xpath(self,rule):
        """
        给response对象添加xpath方法，能够使用xpath提取数据
        :param rule: xpath字符串
        :return: 列表，包含element对象或者
        """
        # print(type(self.body))
        # print(self.body)
        html = etree.HTML(self.body)
        return html.xpath(rule)

    @property  # 转化城属性
    def json(self):
        """
        给response 对象添加json数据，能够直接把响应的json字符串转化成Python类型
        :return:Python类型
        """

        return json.loads(self.body.decode())

    def re_findall(self,rule):
        """
        给response对象添加refindall方法,能够使用正则从响应中提取数据
        :param rule: 正则表达式字符串
        :return: 列表
        """

        return re.findall(rule,self.body.decode())