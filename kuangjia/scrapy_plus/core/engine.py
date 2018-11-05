#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 18-11-2  @Author:libo  @FileName: engine.py

# 引擎组件的封装
from datetime import datetime
import importlib
from scrapy_plus.http.request import Request

from scrapy_plus.core.schedule import Scheduler
from scrapy_plus.core.downloader import Downloader
from scrapy_plus.core.pipeline import Pipeline
from scrapy_plus.middlewares.spidermiddleware import SpiderMiddleware
from scrapy_plus.middlewares.downloadermiddleware import DownloaderMiddleware
import time
from scrapy_plus.conf.settings import SPIDERS, PIPELINES, SPIDER_MIDDLEWARES, DOWNLOADER_MIDDLEWARES,COCOURRENT_REQUEST
from multiprocessing.dummy import Pool




class Engine(object):
    """
    1.对外提供整个程序的如旧
    2.依次调用其他组件对外提供的接口，实现整个框架的运作(驱动)
    """

    def __init__(self):  # 接收外部传入的爬虫对象
        """实例化其他的组件，在引擎中通过调用组件的方法实现其功能"""
        # print(spiders)
        self.scheduler = Scheduler()  # 初始化调度器对象
        self.downloader = Downloader()  # 初始化下载器对象
        self.spiders = self._auto_import_instances(SPIDERS,is_spider=True)  # 爬虫对象 字典
        self.pipelines = self._auto_import_instances(PIPELINES) # 管道对象 列表
        self.spider_mids = self._auto_import_instances(SPIDER_MIDDLEWARES)  # 列表
        self.downloader_mids = self._auto_import_instances(DOWNLOADER_MIDDLEWARES)  # 列表
        self.total_request_nums = 0
        self.total_response_nums = 0
        self.pool = Pool()  # 实例化线程池对象
        self.is_running = False  # 判断程序是否执行标志

    def _auto_import_instances(self, path,is_spider=False):
        """
        实现模块的动态导入，传入模块路径列表，返回类的实例
        :param self:
        :param path:包含模块位置字符串的列表
        :return:{“name”:spider}/[pipeline等]
        """
        if is_spider:
            instances = {}
        else:
            instances = []
        for p in path:
            module_name = p.rsplit(".", 1)[0]  # 获取模块路径的名字
            cls_name = p.rsplit(".", 1)[-1]  # 获取类名
            module = importlib.import_module(module_name)  # 导入模块
            cls = getattr(module, cls_name)  # 获取module下的类
            if is_spider:
                instances[cls().name] = cls()
            else:
                instances.append(cls())
        print(instances)
        return instances

    def start(self):
        """启动整个引擎"""
        start_time = datetime.now()
        print("爬虫启动：", start_time)
        self._start_engine()
        endtime = datetime.now()
        print("爬虫结束：", endtime)
        print(endtime - start_time)
        print("请求数量：", self.total_request_nums)
        print("响应数量：", self.total_response_nums)
        print("重复数量：",self.scheduler.repeat_request_nums)

    def _start_request(self):
        """初始化请求，调用爬虫的start_request方法，把所有等等请求添加到调度器"""
        for spider_name, spider in self.spiders.items():
            for start_request in spider.start_request():

                # 1.对start_request进过爬虫中间件进行处理
                for spider_mid in self.spider_mids:
                    start_request = spider_mid.process_request(start_request)

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
        for downloader_mid in self.downloader_mids:
            request = downloader_mid.process_request(request)

        # 6. 调用下载器的get_response方法，获取响应
        response = self.downloader.get_response(request)

        # 将request的meta值传给response的meta
        response.meta = request.meta

        # 7. response对象经过下载器中间件的process_response进行处理
        for downloader_mid in self.downloader_mids:
            response = downloader_mid.process_response(response)

        # 8. response对象经过下爬虫中间件的process_response进行处理
        for spider_mid in self.spider_mids:
            response = spider_mid.process_response(response)

        # 根据request的spider_name属性获取爬虫实例
        spider = self.spiders[request.spider_name]

        # 获取request对象响应的parse方法
        parse = getattr(spider, request.parse)

        # 9. 调用爬虫的parse方法，处理响应
        for result in parse(response):
            # 判断结果类型，如果是request，重新调用调度器的add_request方法
            if isinstance(result, Request):
                # 在解析函数得到request对象之后，使用process_request进行处理
                for spider_mid in self.spider_mids:
                    result = spider_mid.process_request(result)
                # 为请求对象设置spider_name属性
                result.spider_name = request.spider_name
                # 添加到队列中去
                self.scheduler.add_request(result)
                self.total_request_nums += 1
            # 7如果不是，调用pipeline的process_item方法处理结果
            else:
                for pipeline in self.pipelines:
                    result = pipeline.process_item(result, spider)
        # 响应加1
        self.total_response_nums += 1

    def _callback(self,temp):
        """执行新的请求回调函数，实现循环"""
        if self.is_running is True:
            self.pool.apply_async(self._execute_request_response_item, callback=self._callback)

    def _start_engine(self):
        """依次调用其他组件对外提供的接口，实现整个框架的运作(驱动)"""
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
        self.is_running  = True  # 启动引擎，设置状态为True
        self.pool.apply_async(self._start_request)  # 使用异步,使用子线程
        for i in range(COCOURRENT_REQUEST):
            self.pool.apply_async(self._execute_request_response_item,callback=self._callback)  # 使用子线程


        self._start_request()

        # 设置循环，处理多个请求,阻塞，等待子线程结束
        while True:
            time.sleep(0.0001)

            # self._execute_request_response_item()

            # 设置退出条件：当请求数和响应数相等时，退出循环
            # 因为是异步，需要增加判断条件，请求书不能是0
            # if self.total_response_nums +self.scheduler.repeat_request_nums >= self.total_request_nums:
            # if self.total_response_number >= self.scheduler.total_request_number and self.scheduler.total_request_number != 0:
            if self.total_response_nums >= self.scheduler.total_request_number and self.scheduler.total_request_number != 0:
                self.running = False  # 满足循环退出条件后，设置运行状态为False
                break
