#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 18-11-3  @Author:libo  @FileName: main.py

# project_dir/main.py
from scrapy_plus.core.engine import Engine  # 导入引擎

from spiders import BaiduSpider,QiubaiSpider

if __name__ == '__main__':
    # baidu = BaiduSpider()  # 实例化爬虫对象
    qiubai = QiubaiSpider()
    engine = Engine(qiubai)  # 传入爬虫对象
    engine.start()  # 启动引擎