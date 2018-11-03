#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 18-11-2  @Author:libo  @FileName: schedule.py

# 调度器模块封装
from six.moves.queue import Queue

class Scheduler(object):
    """
    1. 缓存请求对象(request),并为下载器提供请求对象，实现请求的调度
    2. 对请求对象进行去重
    """

    def __init__(self):
        self.queue = Queue()

    def add_request(self,request):
        """添加请求对象"""
        self.queue.put(request)


    def get_request(self):
        """获取一个请求对象并返回"""
        request = self.queue.get()
        return request

    def _filter_request(self):
        """请求去重"""

        pass