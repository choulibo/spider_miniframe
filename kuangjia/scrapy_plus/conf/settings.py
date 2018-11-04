#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 18-11-4  @Author:libo  @FileName: settings.py

# 启用的爬虫类
SPIDERS = [
    'spiders.baidu.BaiduSpider',
    'spiders.qiubai.QiubaiSpider'
]

# 启用的管道类
PIPELINES = [
    'pipelines.BaiduPipelines',
    'pipelines.QIubaiPipelines'
]

# 启用的爬虫中间件类
SPIDER_MIDDLEWARES = [
    "spider_middlewares.TestSpiderMiddleware1"
]

# 启用的下载器中间件类
DOWNLOADER_MIDDLEWARES = [
    "downloader_middlewares.TestDownloaderMiddleware1"
]