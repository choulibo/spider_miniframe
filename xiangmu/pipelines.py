#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 18-11-4  @Author:libo  @FileName: pipelines.py
from spiders.baidu import BaiduSpider
from spiders.qiubai import QiubaiSpider


class BaiduPipelines(object):
    """处理百度数据管道"""

    def process_item(self,item,spider):
        """
        处理item
        :param item: 爬虫爬取的数据
        :param spider: 传递item 的爬虫
        :return: item
        """
        # 这里有所不同的是，需要增加一个参数，也就是传入爬虫对象
        # 以此来判断当前item是属于那个爬虫对象的
        if isinstance(spider,BaiduSpider):
            print("百度管道的数据：",item.data)
        return item  # 交给下一管道

class QIubaiPipelines(object):
    """处理糗百数据的管道"""

    def process_item(self,item,spider):
        """
        处理item
        :param item: 爬虫爬取的数据
        :param spider: 传递item 的爬虫
        :return: item
        """
        if isinstance(spider,QiubaiSpider):
            print("糗百管道的数据：",item.data)
        return item