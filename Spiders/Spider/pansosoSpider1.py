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




class Pansoso1Spider(scrapy.Spider):
    u""" 盘搜搜爬虫01 - 检索输入内容

    """
    name = "pansoso1"
    allowed_domains = ["www.pansoso.com"]
    settings = get_project_settings()

    def __init__(self, search_text='excel', num=1, *args, **kwargs):
        u""" 指定爬虫参数
        exp:
            scrapy crawl myspider -a http_user=myuser -a http_pass=mypassword -a user_agent=mybot

        :param search_text: 搜索内容
        :param num: 查询页数

        """
        super(Pansoso1Spider, self).__init__(*args, **kwargs)
        print('>>>>>>>> @Spider_name: %s @search_text: %s @num: %s'%(self.name, search_text, num))

        start_url = 'http://www.pansoso.com/zh/%s'%search_text
        print('start_url: %s'%start_url)
        self.start_urls = []
        for i in range(1,num+1):
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

    def _prase_prepare(self):
        """ 解析前准备 """

        self.level1_file = self.settings.get('LEVEL1_FILE')
        self.level2_file = self.settings.get('LEVEL2_FILE')
        rm_file(self.level1_file)
        rm_file(self.level2_file)

        write_file(self.level1_file, self.start_urls, mode='override')




# process = CrawlerProcess(settings={
#     'FEED_FORMAT': 'json',
#     'FEED_URI': 'items.json'
# })
# 
# process.crawl(Pansoso1Spider)
# process.start() # the script will block


