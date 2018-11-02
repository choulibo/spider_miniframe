#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 18-11-2  @Author:libo  @FileName: engine.py

# 引擎组件的封装
from scrapy_plus.http.request import Request

from .schedule import Schedule
from .spider import Spider
from .downloader import Downloader
from .pipeline import Pipeline


class Engine(object):
    """
    1.对外提供整个程序的如旧
    2.依次调用其他组件对外提供的接口，实现整个框架的运作(驱动)
    """

    def __init__(self):
        """初始化其他组件对象，在内部使用"""
        self.spider = Spider()
        self.schedule = Schedule()
        self.download = Downloader()
        self.pipeline = Pipeline()

    def start(self):
        """启动整个引擎"""
        self._start_engine()

    def _start_engine(self):

        """依次调用其他组件对外提供的接口，实现整个框架的运作(驱动)"""

        # 1.调用爬虫的start_request方法，获取request对象
        request = self.spider.start_requests()

        # 2.调用调度器的add__request方法,加入到队列中
        self.schedule.add_request(request)

        # 3.调用调度器的get_request方法,获取request对象
        request = self.schedule.get_request()

        # 4.调用下载器的get_response方法,获取响应
        response = self.download.get_response(request)

        # 5.调用爬虫的parse方法,处理响应
        result = self.spider.parse(response)

        # 6.判断结果类型，如果是request，重新调用调度器的add_request方法
        if isinstance(result,Request):
            self.schedule.add_request(result)
        # 7.如果不是,调用pipeline的process_item方法处理结果
        else:
            self.pipeline.process_item(result)

