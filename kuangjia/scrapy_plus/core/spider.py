#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 18-11-2  @Author:libo  @FileName: spider.py

# 爬虫
from scrapy_plus.http.request import Request
from scrapy_plus.item import Item


class Spider:
    '''完成对spider的封装'''
    # start_url = "http://www.baidu.com"  #爬虫最开启请求的url地址

    start_url = []  # 默认初始请求地址

    # def start_requests(self):
    #     '''
    #     构造start_url地址的请求
    #     :return: request
    #     '''
    #     return Request(self.start_url)

    def start_request(self):
        """构建初始请求对象并返回"""
        for url in self.start_url:
            yield Request(url)

    def parse(self, response):
        '''
        默认处理start_url地址对应的响应
        :param response: response对象
        :return: item或者是request
        '''
        yield Item(response.body)
