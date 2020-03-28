# -*- coding: utf-8 -*-
import scrapy
import traceback
from Spider.items import SpiderItem
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import time
import copy
import os

from Spider.spiders.base_func import read_file, write_file, rm_file

class Pansoso2Spider(scrapy.Spider):
    u""" 盘搜搜爬虫02 - 输入页面提取下载信息

    """
    name = "pansoso2"
    allowed_domains = ["www.pansoso.com"]
    settings = get_project_settings()

    level2_file = settings.get('LEVEL2_FILE')
    level3_file = settings.get('LEVEL3_FILE')
    rm_file(level3_file)
    start_urls = read_file(level2_file)
         
    def parse(self, response):
        if response.status == 200:
            selector = scrapy.Selector(response)
            # <div class="down">
            infos = selector.xpath('//div[@class="down"]')
            level3_urls = []
            for info in infos:
                hrefs = info.xpath('a/@href').extract()
                hrefs = [i for i in hrefs if '.html' not in i]
                href = hrefs[0]
                level3_urls.append(href)
            write_file(self.level3_file, level3_urls, mode='append')
        


process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': 'items.json'
})

process.crawl(Pansoso2Spider)
process.start() 
