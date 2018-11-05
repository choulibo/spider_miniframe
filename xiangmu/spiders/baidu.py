#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 18-11-4  @Author:libo  @FileName: baidu.py

from scrapy_plus.core.spider import Spider
from scrapy_plus.http.request import Request
from scrapy_plus.item import Item
import urllib.parse
# 继承框架的爬虫基类
class BaiduSpider(Spider):
    name = "baidu"
    start_urls = ['http://www.baidu.com']* 3  # 设置初始请求url

    def parse(self, response):
        yield Item(response.body[:10])
