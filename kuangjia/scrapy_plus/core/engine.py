#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 18-11-2  @Author:libo  @FileName: engine.py

# 引擎组件的封装
from datetime import datetime

from scrapy_plus.http.request import Request

from scrapy_plus.core.schedule import Scheduler
from scrapy_plus.core.downloader import Downloader
from scrapy_plus.core.pipeline import Pipeline
from scrapy_plus.middlewares.spidermiddleware import SpiderMiddleware
from scrapy_plus.middlewares.downloadermiddleware import DownloaderMiddleware
import time

class Engine(object):
    """
    1.对外提供整个程序的如旧
    2.依次调用其他组件对外提供的接口，实现整个框架的运作(驱动)
    """

    def __init__(self, spiders):  # 接收外部传入的爬虫对象
        self.spiders = spiders  # 爬虫对象
        self.scheduler = Scheduler()  # 初始化调度器对象
        self.downloader = Downloader()  # 初始化下载器对象
        self.pipeline = Pipeline()  # 初始化管道对象

        self.spider_mid = SpiderMiddleware()
        self.downloader_mid = DownloaderMiddleware()
        self.total_request_nums = 0
        self.total_response_nums = 0

    def start(self):
        """启动整个引擎"""
        start_time = datetime.now()
        print("爬虫启动：",start_time)
        self._start_engine()
        endtime = datetime.now()
        print("爬虫结束：",endtime)
        print(endtime-start_time)
        print("请求数量：",self.total_request_nums)
        print("响应数量：",self.total_response_nums)

    def _start_request(self):
        """初始化请求，调用爬虫的start_request方法，把所有等等请求添加到调度器"""
        for spider_name,spider in self.spiders.items():
            for start_request in spider.start_request():

                # 1.对start_request进过爬虫中间件进行处理
                start_request = self.spider_mid.process_request(start_request)

                # 给请求对象添加spider_name 属性
                start_request.spider_name = spider_name

                # 2. 调用调度器的add_request方法，添加request对象到调度器中
                self.scheduler.add_request(start_request)

                # 3.请求数加1
                self.total_request_nums += 1


    def _execute_request_response_item(self):

        # 4.调用调度器的get_request方法，获取request
        request = self.scheduler.get_request()

        # 判断请求对象是否存在,不存在，直接返回
        if request is None:
            return

        # 5. request对象经过下载器中间件的process_request进行处理
        request = self.downloader_mid.process_request(request)

        # 6. 调用下载器的get_response方法，获取响应
        response = self.downloader.get_response(request)

        # 将request的meta值传给response的meta
        response.meta = request.meta

        # 7. response对象经过下载器中间件的process_response进行处理
        response = self.downloader_mid.process_response(response)

        # 8. response对象经过下爬虫中间件的process_response进行处理
        response = self.spider_mid.process_response(response)

        # 根据request的spider_name属性获取爬虫实例
        spider = self.spiders[request.spider_name]

        # 获取request对象响应的parse方法
        parse = getattr(spider,request.parse)


        # 9. 调用爬虫的parse方法，处理响应
        for result in parse(response):
            # 判断结果类型，如果是request，重新调用调度器的add_request方法
            if isinstance(result,Request):
                # 在解析函数得到request对象之后，使用process_request进行处理
                result = self.spider_mid.process_request(result)
                # 为请求对象设置spider_name属性
                result.spider_name = request.spider_name
                # 添加到队列中去
                self.scheduler.add_request(result)
                self.total_request_nums += 1
            # 7如果不是，调用pipeline的process_item方法处理结果
            else:
                self.pipeline.process_item(result)
        # 响应加1
        self.total_response_nums += 1

    def _start_engine(self):

        """具体实现引擎的细节"""

        #"""依次调用其他组件对外提供的接口，实现整个框架的运作(驱动)"""
        #
        # # 1. 调用爬虫的start_request方法，获取request对象
        # start_request = self.spider.start_requests()
        # # 对start_request进过爬虫中间件进行处理
        # start_request = self.spider_mid.process_request(start_request)
        #
        # # 2. 调用调度器的add_request方法，添加request对象到调度器中
        # self.scheduler.add_request(start_request)
        # # 3. 调用调度器的get_request方法，获取request对象
        # request = self.scheduler.get_request()
        # # request对象经过下载器中间件的process_request进行处理
        # request = self.downloader_mid.process_request(request)
        #
        # # 4. 调用下载器的get_response方法，获取响应
        # response = self.downloader.get_response(request)
        # # response对象经过下载器中间件的process_response进行处理
        # response = self.downloader_mid.process_response(response)
        # # response对象经过下爬虫中间件的process_response进行处理
        # response = self.spider_mid.process_response(response)
        #
        # # 5. 调用爬虫的parse方法，处理响应
        # result = self.spider.parse(response)
        # # 6.判断结果的类型，如果是request，重新调用调度器的add_request方法
        # if isinstance(result, Request):
        #     # 在解析函数得到request对象之后，使用process_request进行处理
        #     result = self.spider_mid.process_request(result)
        #     self.scheduler.add_request(result)
        # # 7如果不是，调用pipeline的process_item方法处理结果
        # else:
        #     self.pipeline.process_item(result)

        self._start_request()

        while True:
            time.sleep(0.001)

            self._execute_request_response_item()

            if self.total_response_nums>=self.total_request_nums:
                break
