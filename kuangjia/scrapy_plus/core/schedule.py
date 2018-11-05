#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 18-11-2  @Author:libo  @FileName: schedule.py

# 调度器模块封装
from six.moves.queue import Queue
import w3lib.url
from hashlib import sha1
import six

def _to_bytes(string):
    """对数据进行转码"""

    if six.PY2:
        # 当前环境是Python2
        if isinstance(string,str):
            return string
        else:
            return string.encode("utf-8")
    if six.PY3:
        if isinstance(string,str):
            return string.encode("utf-8")
        else:
            return string

class Scheduler(object):
    """
    1. 缓存请求对象(request),并为下载器提供请求对象，实现请求的调度
    2. 对请求对象进行去重
    """

    def __init__(self):
        self.queue = Queue()
        # 记录总共的请求数
        self.total_request_number = 0
        self._filter_container = set()
        # 统计请求重复的数量
        self.repeat_request_nums = 0

    def add_request(self,request):
        """添加请求对象"""
        if self._filter_request(request):
            self.queue.put(request)
            self.total_request_number += 1  #  统计请求总数

    def get_request(self):
        """获取一个请求对象并返回"""
        try:
            # 设置非堵塞
            request = self.queue.get(block=False)
        except:
            return None
        else:
            return request

    def _filter_request(self,request):
        """
        判断请求对象是否重复
        :param request: 请求对象
        :return: bool类型
        """

        # 对request对象添加一个fp属性，添加指纹
        request.fp = self._gen_fp(request)
        # print(request.fp,self._filter_container)
        if request.fp not in  self._filter_container:
            # 判断指纹不在指纹集合中,将指纹加入到集合中
            self._filter_container.add(request.fp)
            return True
        else:
            print("重复的请求：{},{}".format(request.method,request.url))
            self.repeat_request_nums += 1


    def _gen_fp(self,request):
        """
        生成request对象的指纹
        :param request:request对象
        :return:指纹，字符串
        """

        # 对请求头,请求URL,请求参数,请求方法进行加密，得到指纹

        # 对URL进行排序
        url = w3lib.url.canonicalize_url(request.url)
        # 对请求方法
        method = request.method.upper()
        # 对请求参数
        params = request.params if request.params is not None else {}
        params = str(sorted(params.items(),key=lambda x:x[0]))

        # 对请求体进行排序
        data = request if request.data is not None else {}
        data = str(sorted(data.items(),key=lambda x:x[0]))

        # 使用sha1对数据进行加密
        fp = sha1()
        # 添加url地址
        fp.update(_to_bytes(url))
        # 添加请求方法
        fp.update(_to_bytes(method))
        # 添加请求体
        fp.update(_to_bytes(data))
        # 添加请求参数
        fp.update(_to_bytes(params))
        # 返回16进制字符串
        return fp.hexdigest()

