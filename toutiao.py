#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 18-11-29  @Author:libo  @FileName: toutiao.py

import requests
import os
from hashlib import md5
from urllib.parse import urlencode
from multiprocessing import Pool


def get_page(offset):
    """单页"""
    params = {
        "offset": offset,
        "format": "json",
        "keyword": "街拍",
        "count": "20",
        "curtab": "3"
    }

    url = "https://www.toutiao.com/search_content/?" + urlencode(params)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None


def get_images(json):
    if json.get("data"):
        for item in json.get("data"):
            title = item.get("title")
            images = item.get("image_list")
            for image in images:
                yield {
                    "image": image.get("url"),
                    "title": title
                }


def save_image(item):
    if not os.path.exists(item.get("title")):
        os.mkdir(item.get("title"))
    try:
        response = requests.get(item.get("image"))
        if response.status_code == 200:
            file_path = "{}/{}.{}".format(item.get("title"), md5(response.content).hexdigest(), "jpg")
            print(file_path)
            if not os.path.exists(file_path):
                with open('file_path', "wb") as f:
                    f.write(response.content)
            else:
                print("Done", file_path)
    except requests.ConnectionError:
        print("Failed")


def main(offset):
    json = get_page(offset)
    for item in get_images(json):
        # print(item)
        save_image(item)


GROUP_START = 1
GROUP_END = 20

if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END)])
    pool.map(main, groups)
    pool.close()
    pool.join()
