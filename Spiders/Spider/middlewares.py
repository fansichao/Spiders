# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import time
import random  
import scrapy  
from scrapy import signals
from  scrapy.http import HtmlResponse
from scrapy.utils.project import get_project_settings

from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError
from selenium.common.exceptions import TimeoutException


settings = get_project_settings()

class SpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SpiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        
        # scfan 破解反爬虫机制-防盗链
        referer = request.url
        if referer:
            request.headers['referer'] = referer

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


 

 
class ProxyMiddleWare(object):  
    """ IP 代理中间件 """  
    ALL_EXCEPTIONS = (defer.TimeoutError, TimeoutError, DNSLookupError,
                      ConnectionRefusedError, ConnectionDone, ConnectError,
                      ConnectionLost, TCPTimedOutError, ResponseFailed,
                      IOError, TunnelError)
 
    def __init__(self):
        pass

    def process_request(self,request, spider):  
        '''对request对象加上proxy'''  
        proxy = self.get_random_proxy()  
        if settings.get("IS_USE_PROXY", False):
            spider.logger.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 已开启代理服务')
            print("this is request ip:"+proxy)  
            request.meta['proxy'] = proxy   

            # 解决 页面延迟加载问题
            try:
                if settings.get("IS_USE_DELAY_LOAD_URL", False):
                    try:
                        spider.browser.get(request.url)
                        time.sleep(settings.get("DELAY_LOAD_URL_TIME_first", 3))
                        spider.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                        #执行页面下拉操作的代码
                    except TimeoutException as e:
                        print('超时')
                        spider.browser.execute_script('window.stop()')
                    time.sleep(settings.get("DELAY_LOAD_URL_TIME_second", 2))
                    return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source,
                                        encoding="utf-8", request=request)
            except Exception as err:
                pass
        else:
            spider.logger.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 未开启代理服务')
    



    def process_response(self, request, response, spider):  
        '''对返回的response处理'''  
        # 如果返回的response状态不是200，重新生成当前request对象  
        if settings.get("IS_USE_PROXY", False):
            if response.status != 200:  
                proxy = self.get_random_proxy()  
                print("this is response ip:"+proxy)  
                # 对当前reque加上代理  
                request.meta['proxy'] = proxy   
                return request  
        return response  

    def get_random_proxy(self):  
        '''随机从文件中读取proxy'''  
        while 1:  
            with open(settings.get('PROXY_FILE_NAME'), 'r') as f:  
                proxies = f.readlines()  
            if proxies:  
                break  
            else:  
                time.sleep(1)  
        proxy = random.choice(proxies).strip()  
        return proxy  
 
    def process_exception(self, request, exception, spider):
        """ 捕获几乎所有的异常 """
        if isinstance(exception, self.ALL_EXCEPTIONS):
            spider.logger.error('Error: Got exception: %s' % (exception))
            response = HtmlResponse(url='exception')

            # 重新请求
            request.meta['proxy'] = self.get_random_proxy()
            return response
        spider.logger.error('not contained exception: %s' % exception)
 
