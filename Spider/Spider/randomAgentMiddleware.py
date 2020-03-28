# -*- coding: utf-8 -*-
import scrapy
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random
 
 
 
class MyUserAgentMiddleware(UserAgentMiddleware):
    '''
    设置User-Agent
    '''
 
    def __init__(self, user_agent):
        self.user_agent = user_agent
 
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent=crawler.settings.get('USER_AGENT_LIST')
        )
 
    def process_request(self, request, spider):
        agent = random.choice(self.user_agent)
        request.headers['User-Agent'] = agent
