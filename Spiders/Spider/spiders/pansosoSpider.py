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

settings = get_project_settings()

from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging



class PansosoSpider1(scrapy.Spider):
    u""" 盘搜搜爬虫01 - 检索输入内容

    """
    name = "pansoso01"
    allowed_domains = ["www.pansoso.com"]

    def __init__(self, search_text='excel', page=1, *args, **kwargs):
        u""" 指定爬虫参数
        exp:
            scrapy crawl myspider -a http_user=myuser -a http_pass=mypassword -a user_agent=mybot

        :param search_text: 搜索内容
        :param page: 查询页数

        """
        super(PansosoSpider1, self).__init__(*args, **kwargs)
        print('>>>>>>>> @Spider_name: %s @search_text: %s @page: %s'%(self.name, search_text, page))

        start_url = 'http://www.pansoso.com/zh/%s'%search_text
        print('start_url: %s'%start_url)
        self.start_urls = []
        for i in range(1,page+1):
            self.start_urls.append(start_url+'_%s'%i)

    def parse(self, response):

        self._prase_prepare()

        print('>>>>>>>>> panpan1 parse')
        if response.status == 200:
            selector = scrapy.Selector(response)

            # <div class="pss">
            infos = selector.xpath('//div[@class="pss"]')
            level2_urls = []
            for info in infos:
                # item = scrapy.JsuserItem()
                href = info.xpath('h2/a/@href').extract()[0]
                level2_urls.append(href)
                print(href)
                SpiderItem.href = href
            write_file(self.level2_file, level2_urls, mode='append')
            print("写入文件[%s]成功" % self.level2_file)

    def _prase_prepare(self):
        """ 解析前准备 """

        self.level1_file = settings.get('LEVEL1_FILE')
        self.level2_file = settings.get('LEVEL2_FILE')
        rm_file(self.level1_file)
        rm_file(self.level2_file)

        write_file(self.level1_file, self.start_urls, mode='override')
        print("写入文件[%s]成功" % self.level1_file)

class PansosoSpider2(scrapy.Spider):
    u""" 盘搜搜爬虫02 - 输入页面提取下载信息

    """
    name = "pansoso02"
    allowed_domains = ["www.pansoso.com"]

    def __init__(self, *args, **kwargs):
        super(PansosoSpider2, self).__init__(*args, **kwargs)

        self.level2_file = settings.get('LEVEL2_FILE')
        self.level3_file = settings.get('LEVEL3_FILE')
        rm_file(self.level3_file)
        self.start_urls = read_file(self.level2_file)

        print('>>>>>>>>>>>>> 2')
        print(dir(self))
        print(dir(self.start_requests))
        print(self.start_requests)
         
    def parse(self, response):
        if response.status == 200:
            selector = scrapy.Selector(response)
            # <div class="down">
            infos = selector.xpath('//div[@class="down"]')
            print('>>>>>> ssssssssssssssss')
            print(infos)
            print(response.text)
        

            level3_urls = []
            for info in infos:
                hrefs = info.xpath('a/@href').extract()
                hrefs = [i for i in hrefs if '.html' not in i]
                href = hrefs[0]
                level3_urls.append(href)
            write_file(self.level3_file, level3_urls, mode='append')
            print("写入文件[%s]成功" % self.level3_file)
        

class PansosoSpider3(scrapy.Spider):
    u""" 盘搜搜爬虫03 - 提取百度云链接

    """
    name = "pansoso03"
    allowed_domains = ["www.pansoso.com"]

    def __init__(self, *args, **kwargs):
        super(PansosoSpider3, self).__init__(*args, **kwargs)

        self.level3_file = settings.get('LEVEL3_FILE')
        self.level4_file = settings.get('LEVEL4_FILE')
        rm_file(self.level4_file)
        self.start_urls = read_file(self.level3_file)
         
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
            print("写入文件[%s]成功" % self.level4_file)

if __name__ == '__main__':
    pass

