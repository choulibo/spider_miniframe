#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 18-11-3  @Author:libo  @FileName: spiders.py

from scrapy_plus.core.spider import Spider


# 继承框架的爬虫基类
class BaiduSpider(Spider):

    start_url = ['http://www.douban.com']* 5  # 设置初始请求url