#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 18-11-2  @Author:libo  @FileName: request.py


class Request:
    '''完成对请求对象的封装'''

    def __init__(self, url, method="GET", headers=None, params=None, data=None, parse='parse',meta = None):
        '''
        初始化request对象
        :param url: url地址
        :param method: 请求方法
        :param headers: 请求头
        :param params: 请求的参数
        :param data: 请求体
        :param parse: 请求对象的响应函数名
        :param meta: 不同解析函数间传递数据
        '''
        self.url = url
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data
        self.parse = parse  # 指明它的解析函数, 默认是parse方法
        self.meta = meta