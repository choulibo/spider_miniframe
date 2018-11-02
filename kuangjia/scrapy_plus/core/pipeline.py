#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 18-11-2  @Author:libo  @FileName: pipeline.py


# 管道组件的封装

class Pipeline(object):
    """负责处理数据对象(item)"""

    def process_item(self,item):
        """处理item对象"""

        print("item:",item)