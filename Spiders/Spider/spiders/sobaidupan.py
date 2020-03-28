# -*- coding: utf-8 -*-
u"""

百度网盘资源搜索
    https://www.sobaidupan.com/

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

class SobaidupanSpider1(scrapy.Spider):
    u""" 搜百度盘 01 - 检索输入内容

    """
    name = "sobaidupan01"
    allowed_domains = ["www.sobaidupan.com"]

    def __init__(self, search_text='excel', page=1, mode='append', *args, **kwargs):
        u""" 指定爬虫参数
        exp:
            scrapy crawl myspider -a http_user=myuser -a http_pass=mypassword -a user_agent=mybot

        :param search_text: 搜索内容
        :param page: 查询页数
        :param mode: override / append 覆盖 or 追加

        """
        page = int(page)
        self.mode = mode

        super(SobaidupanSpider1, self).__init__(*args, **kwargs)
        print('>>>>>>>> @Spider_name: %s @search_text: %s @page: %s'%(self.name, search_text, page))

        start_url = 'https://www.sobaidupan.com/search.asp?wd=%s'%(search_text)
        self.start_urls = []
        for i in range(1, page+1):
            self.start_urls.append(start_url+'&page=%s'%i)

        self._prase_prepare()

    def parse(self, response):

        if response.status == 200:
            selector = scrapy.Selector(response)
            infos = selector.xpath('//div[@class="search_box_list_bt"]')
                
            level2_urls = []
            for info in infos:
                # item = scrapy.JsuserItem()
                href = info.xpath('a/@href').extract()[0]
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

class SobaidupanSpider2(scrapy.Spider):
    u""" 盘搜搜爬虫02 - 输入页面提取下载信息

    """
    name = "sobaidupan02"
    allowed_domains = ["www.sobaidupan.com"]

    def __init__(self, mode='append', *args, **kwargs):
        super(SobaidupanSpider2, self).__init__(*args, **kwargs)

        self.mode = mode
        self.level2_file = settings.get('LEVEL2_FILE')
        self.level3_file = settings.get('LEVEL3_FILE')
        if self.mode == 'override':
            rm_file(self.level3_file)
        self.start_urls = read_file(self.level2_file)
         
    def parse(self, response, autorun=True):
        u"""
        说明：
            1. 由于此网站 此链接 会自动跳转百度网盘
            所以直接获取 访问的url 即可
        exp:
            原链接: http://w.sbdp.hao7188.com/down.asp?id=109483377&token=803676c3cd6a8eb8d15a41ba79e85da1&bt=Excel%E5%A4%8D%E4%B9%A0.rar
            自动跳转: https://yun.baidu.com/s/1c0b2Oec

        """
        level3_urls = []

        if response.status == 200:
            selector = scrapy.Selector(response)

            if autorun:
                href = response.url
                if '404.html' not in href and True not in [i in href for i in self.allowed_domains]:
                    level3_urls.append(href)
            else:
                infos = selector.xpath('//p[@style="text-align:center;"]')

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

