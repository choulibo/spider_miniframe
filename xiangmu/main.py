#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 18-11-3  @Author:libo  @FileName: main.py

# project_dir/main.py
from scrapy_plus.core.engine import Engine  # 导入引擎

from spiders.baidu import BaiduSpider
from spiders.qiubai import QiubaiSpider
from pipelines import BaiduPipelines,QIubaiPipelines
from spider_middlewares import TestSpiderMiddleware1,TestSpiderMiddleware2
from downloader_middlewares import TestDownloaderMiddleware1,TestDownloaderMiddleware2


if __name__ == '__main__':
    baidu = BaiduSpider()  # 实例化爬虫对象
    qiubai = QiubaiSpider()
    spiders = {baidu.name:baidu,qiubai.name:qiubai}
    pipelines = [BaiduPipelines(),QIubaiPipelines()]
    spider_mids = [TestSpiderMiddleware1(),TestSpiderMiddleware2()]
    downloader_mids = [TestDownloaderMiddleware1(),TestDownloaderMiddleware2()]
    engine = Engine(pipelines = pipelines,spider_mids = spider_mids,downloader_mids = downloader_mids)  # 传入爬虫对象
    engine.start()  # 启动引擎