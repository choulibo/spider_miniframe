#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 18-11-2  @Author:libo  @FileName: engine.py

# 引擎组件的封装
from scrapy_plus.http.request import Request

from scrapy_plus.core.schedule import Scheduler
from scrapy_plus.core.spider import Spider
from scrapy_plus.core.downloader import Downloader
from scrapy_plus.core.pipeline import Pipeline
from scrapy_plus.middlewares.spidermiddleware import SpiderMiddleware
from scrapy_plus.middlewares.downloadermiddleware import DownloaderMiddleware

class Engine(object):
    """
    1.对外提供整个程序的如旧
    2.依次调用其他组件对外提供的接口，实现整个框架的运作(驱动)
    """

    def __init__(self, spider):  # 接收外部传入的爬虫对象
        self.spider = spider  # 爬虫对象
        self.scheduler = Scheduler()  # 初始化调度器对象
        self.downloader = Downloader()  # 初始化下载器对象
        self.pipeline = Pipeline()  # 初始化管道对象

        self.spider_mid = SpiderMiddleware()
        self.downloader_mid = DownloaderMiddleware()

    def start(self):
        """启动整个引擎"""
        self._start_engine()

    def _start_engine(self):

        """依次调用其他组件对外提供的接口，实现整个框架的运作(驱动)"""

        # 1. 调用爬虫的start_request方法，获取request对象
        start_request = self.spider.start_requests()
        # 对start_request进过爬虫中间件进行处理
        start_request = self.spider_mid.process_request(start_request)

        # 2. 调用调度器的add_request方法，添加request对象到调度器中
        self.scheduler.add_request(start_request)
        # 3. 调用调度器的get_request方法，获取request对象
        request = self.scheduler.get_request()
        # request对象经过下载器中间件的process_request进行处理
        request = self.downloader_mid.process_request(request)

        # 4. 调用下载器的get_response方法，获取响应
        response = self.downloader.get_response(request)
        # response对象经过下载器中间件的process_response进行处理
        response = self.downloader_mid.process_response(response)
        # response对象经过下爬虫中间件的process_response进行处理
        response = self.spider_mid.process_response(response)

        # 5. 调用爬虫的parse方法，处理响应
        result = self.spider.parse(response)
        # 6.判断结果的类型，如果是request，重新调用调度器的add_request方法
        if isinstance(result, Request):
            # 在解析函数得到request对象之后，使用process_request进行处理
            result = self.spider_mid.process_request(result)
            self.scheduler.add_request(result)
        # 7如果不是，调用pipeline的process_item方法处理结果
        else:
            self.pipeline.process_item(result)

