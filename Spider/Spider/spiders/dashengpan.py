# -*- coding: utf-8 -*-
u"""

大圣盘 网盘资源搜索
    https://www.dashengpan.com/

"""
import time
import copy
import os
import traceback

import scrapy
from Spider.items import SpiderItem
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
 
from Spider.spiders.base_func import read_file, write_file, rm_file
from twisted.internet import reactor
from scrapy.utils.log import configure_logging

settings = get_project_settings()

class DashengpanSpider1(scrapy.Spider):
    u""" 检索输入内容

    """
    name = "dashengpan01"
    allowed_domains = ["www.dashengpan.com"]

    def __init__(self, search_text='excel', num=1, mode='append', *args, **kwargs):
        u""" 指定爬虫参数
        exp:
            scrapy crawl myspider -a http_user=myuser -a http_pass=mypassword -a user_agent=mybot

        :param search_text: 搜索内容
        :param num: 查询页数
        :param mode: override / append 覆盖 or 追加

        """
        num = int(num)
        self.mode = mode
        self.base_url = "https://www.dashengpan.com"

        super(SobaidupanSpider1, self).__init__(*args, **kwargs)
        print('>>>>>>>> @Spider_name: %s @search_text: %s @num: %s'%(self.name, search_text, num))

        start_url = 'https://www.dashengpan.com/search?keyword=%s'%(search_text)

        self.start_urls = []
        for i in range(1,num+1):
            self.start_urls.append(start_url+'&page=%s'%i)

        self._prase_prepare()

    def parse(self, response):

        if response.status == 200:
            selector = scrapy.Selector(response)
            infos = selector.xpath('//div[@class="resource-info"]')
                
            level2_urls = []
            for info in infos:
                # item = scrapy.JsuserItem()
                href = self.base_url + info.xpath('h1/a/@href').extract()[0]
                level2_urls.append(href)
                SpiderItem.href = href
            write_file(self.level2_file, level2_urls, mode='append')
            print("写入文件[%s]成功" % self.level2_file)

    def _prase_prepare(self):
        """ 解析前准备 """

        self.level1_file = settings.get('LEVEL1_FILE')
        self.level2_file = settings.get('LEVEL2_FILE')
        if self.mode == 'override':
            rm_file(self.level1_file)
            rm_file(self.level2_file)

        write_file(self.level1_file, self.start_urls, mode=self.mode)
        print("写入文件[%s]成功" % self.level1_file)

class DashengpanSpider2(scrapy.Spider):
    u""" 盘搜搜爬虫02 - 输入页面提取下载信息

    """
    name = "dashengpan02"
    allowed_domains = ["www.dashengpan.com"]

    def __init__(self, mode='append', *args, **kwargs):
        super(SobaidupanSpider2, self).__init__(*args, **kwargs)

        self.mode = mode
        self.level2_file = settings.get('LEVEL2_FILE')
        self.level3_file = settings.get('LEVEL3_FILE')
        if self.mode == 'override':
            rm_file(self.level3_file)
        self.start_urls = read_file(self.level2_file)
         
    def parse(self, response):
        u"""

        """
        level3_urls = []
        print(dir(response))
        if response.status == 200 and '该链接有效，可以访问' in response.text():
            selector = scrapy.Selector(response)
            infos = selector.xpath('//div[@class="meta-item copy-item"]')

            for info in infos:
                hrefs = info.xpath('a/@href').extract()
                hrefs = [i for i in hrefs if '.html' not in i]
                href = hrefs[0]
                if '404.html' not in href:
                    level3_urls.append(href)

            write_file(self.level3_file, level3_urls, mode='append')
            print("写入文件[%s]成功" % self.level3_file)
        


if __name__ == '__main__':
    pass

