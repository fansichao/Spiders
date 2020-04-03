# -*- coding: utf-8 -*-
u"""

大圣盘 网盘资源搜索
    https://www.dashengpan.com/

"""
import time
import copy
import os
import traceback

from lxml import html
import re
import scrapy
from Spider.items import SpiderItem
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
 
from scrapy.utils.log import configure_logging
from Spider.spiders.base_func import read_file, write_file, rm_file
from twisted.internet import reactor
from selenium import webdriver

settings = get_project_settings()

class DashengpanSpider1(scrapy.Spider):
    u""" 检索输入内容

    """
    name = "dashengpan01"
    allowed_domains = ["www.dashengpan.com"]

    def __init__(self, search_text='excel', page=1, mode='append', *args, **kwargs):
        u""" 指定爬虫参数
        exp:
            scrapy crawl myspider -a http_user=myuser -a http_pass=mypassword -a user_agent=mybot

        :param search_text: 搜索内容
        :param page: 查询页数
        :param mode: override / append 覆盖 or 追加

        """
        super(DashengpanSpider1, self).__init__(*args, **kwargs)

        page = int(page)
        self.mode = mode
        self.base_url = "https://www.dashengpan.com"
        self.level1_file = settings.get('LEVEL1_FILE')
        self.level2_file = settings.get('LEVEL2_FILE')

        print('>>>>>>>> @Spider_name: %s @search_text: %s @page: %s'%(self.name, search_text, page))
        start_url = 'https://www.dashengpan.com/search?keyword=%s'%(search_text)
        http_dic = {
            ' ':'%20',
        }
        for key,val in list(http_dic.items()):
            start_url = start_url.replace(key,val)
        self.start_urls = []
        for i in range(1,page+1):
            self.start_urls.append(start_url+'&page=%s'%i)


        if self.mode == 'override':
            rm_file(self.level1_file)

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

        if self.mode == 'override':
            rm_file(self.level2_file)

        write_file(self.level1_file, self.start_urls, mode=self.mode)
        print("写入文件[%s]成功" % self.level1_file)

class DashengpanSpider2(scrapy.Spider):
    u""" 盘搜搜爬虫02 - 输入页面提取下载信息

    """
    name = "dashengpan02"
    allowed_domains = ["www.dashengpan.com"]

    def __init__(self, mode='append', *args, **kwargs):
        super(DashengpanSpider2, self).__init__(*args, **kwargs)

        self.mode = mode
        self.level2_file = settings.get('LEVEL2_FILE')
        self.result_file = settings.get('RESULT_FILE')
        if self.mode == 'override':
            rm_file(self.result_file)
        self.start_urls = read_file(self.level2_file)
        self.start_urls = [i for i in self.start_urls if i.startswith('http')]

        if settings.get("IS_USE_DELAY_LOAD_URL", False):
            # 延迟加载
            self.browser = webdriver.Chrome()
            self.browser.set_page_load_timeout(30)
         
    def parse(self, response):
        u"""

        说明:
            1. 大圣盘 自带链接校验机制 
                HTML中含 该链接有效，可以访问 ,说明链接有效 
            2. 反爬虫机制
                1. 延迟加载 

        提取码HTML
            <div class="resource-meta" data-v-7b9e41d7="">
                <span data-v-7b9e41d7="" class="meta-item copy-item">
                    <span data-v-7b9e41d7="" class="label">提取密码</span> 
                    h99f 
                    <span data-v-7b9e41d7="" class="copy">点击复制</span>
                </span> 
                <span data-v-7b9e41d7="" class="tip">提取码复制成功</span>
            </div>
    
        """
        result_url = []
        get_code_flag = get_url_flag = True
        #if response.status == 200 and '该链接有效，可以访问' in response.text:
        if response.status == 200:
            selector = scrapy.Selector(response)
            code = ''
            
            try:
                # 提取码
                if get_code_flag:
                    code_infos = selector.xpath('//div[@class="resource-meta"]')
                    # code_info_str = str(code_infos.extract()[0], encoding='utf-8')
                    if bool(code_infos.extract()):
                        code_info_str = code_infos.extract()[0]#.decode()

                        reg = '    \S{4} '
                        lis = re.findall(reg, code_info_str, re.I)
                        lis = [i.strip() for i in lis if i and len(i.strip()) == 4]
                        code = lis[0] if bool(lis) else ''
            except Exception as err:
                print('>> 获取提取码失败!: \n%s'%err)
                print(traceback.format_exc())

            try:
                # 链接
                if get_url_flag:
                    selector = scrapy.Selector(response)
                    # url_infos = selector.xpath('//div[@class="button-inner baidu-button-inner"]')
                    url_infos = selector.xpath('//div[@class="button-inner"]')
                    print(url_infos)
                    for url_info in url_infos:
                        urls = url_info.xpath('a/@href').extract()
                        urls = [i for i in urls if '.html' not in i and 'baidu' in i]
                        if not bool(urls):
                            continue
                        url = urls[0]
                        href =  url + ' ' + code
                        print('> 获取链接: %s 提取码: %s'%(url ,code))
                        result_url.append(href)
                                
                if bool(result_url):
                    write_file(self.result_file, result_url, mode='append')
                    print("写入文件[%s]成功" % self.result_file)
            except Exception as err:
                print('>> 获取链接失败!: \n%s'%err)
                print(traceback.format_exc())
        
        else:
            print("该链接[%s]已失效 or 未使用延迟加载处理 IS_USE_DELAY_LOAD_URL" % response.url)
        

if __name__ == '__main__':
    pass

