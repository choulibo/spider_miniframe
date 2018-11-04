#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 18-11-4  @Author:libo  @FileName: spider_middlewares.py

class TestSpiderMiddleware1:
    """实现下载器中间件"""

    def process_request(self,request):
        """
        处理请求
        :param request:
        :return:
        """
        # print("TestSpiderMiddleware1--process_request")
        return request

    def process_response(self,response):
        """
        处理响应
        :param response: 响应对象
        :return: 响应对象
        """
        # print("TestSpiderMiddleware1--process_response")
        return response

class TestSpiderMiddleware2:
    """实现下载器中间件"""

    def process_request(self, request):
        """
        处理请求
        :param request:
        :return:
        """
        # print("TestSpiderMiddleware2--process_request")
        return request

    def process_response(self, response):
        """
        处理响应
        :param response: 响应对象
        :return: 响应对象
        """
        # print("TestSpiderMiddleware2--process_response")
        return response