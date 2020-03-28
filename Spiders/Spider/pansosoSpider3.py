# -*- coding: utf-8 -*-
import scrapy
import traceback
from Spider.items import SpiderItem
from scrapy.utils.project import get_project_settings
import time
import copy
import os

from Spider.spiders.base_func import read_file, write_file, rm_file

class PansosoSpiderThread(scrapy.Spider):
    u""" 盘搜搜爬虫03 - 提取百度云链接

    """
    name = "pansoso3"
    allowed_domains = ["www.pansoso.com"]

    settings = get_project_settings()
    level3_file = settings.get('LEVEL3_FILE')
    level4_file = settings.get('LEVEL4_FILE')
    rm_file(level4_file)
    start_urls = read_file(level3_file)
         
    def parse(self, response):
        time.sleep(0.5)
        if response.status == 200:
            selector = scrapy.Selector(response)

            infos = selector.xpath('//div[@class="file"]')
            level4_urls = []
            for info in infos:
                href = info.xpath('p/a/@href').extract()[0]
                print(href)
                level4_urls.append(href)
            write_file(self.level4_file, level4_urls, mode='append')

