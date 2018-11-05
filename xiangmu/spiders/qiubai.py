#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 18-11-4  @Author:libo  @FileName: qiubai.py

from scrapy_plus.core.spider import Spider
from scrapy_plus.http.request import Request
from scrapy_plus.item import Item
import urllib.parse

class QiubaiSpider(Spider):
    name = "qiubai"
    start_urls = []

    def start_request(self):
        """发送start_urls中url地址的请求"""

        url_temp = "https://www.qiushibaike.com/8hr/page/{}/"
        # yield Request(url_temp)
        for i in range(1,14):
            yield Request(url_temp.format(i))

    def parse(self, response):
        """提取页面的数据"""
        # 先分组，在提取数据
        div_list = response.xpath("//div[@id='content-left']/div")
        # print(len(div_list))
        for div in div_list[:1]:
            item = {}
            item["name"] = div.xpath(".//h2/text()")[0].strip()
            item["age"] = div.xpath(".//div[contains(@class,'articleGender')]/text()")
            item["age"] = item["age"][0] if len(item["age"])>0 else None
            item["gender"] = div.xpath(".//div[contains(@class,'articleGender')]/@class")
            # item["gender"] = item["gender"][0].split(' ')[-1].replace("Icon", "") if len(["gender"]) > 0 else None
            item["gender"] = item["gender"][0].split(" ")[-1].replace("Icon", "") if len(item["gender"]) > 0 else None
            item["href"] = urllib.parse.urljoin(response.url,div.xpath("./a/@href")[0])
            # print(item)
            yield Item(item)
            yield Request(item["href"], parse="parse_detail", meta={"item": item})


    def parse_detail(self,response):
        """详情页响应函数"""
        item = response.meta["item"]
        item["stats_vote"] = response.xpath("//span[@class='stats-vote']/i/text()")
        item["stats_vote"] = item["stats_vote"][0] if len(item["stats_vote"])>0 else None
        yield Item(item)