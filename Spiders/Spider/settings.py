# -*- coding: utf-8 -*-

# Scrapy settings for Spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

# >>>>>>>>>>>> Spider Settings Start 爬虫级别配置

# 爬虫配置参考链接: https://blog.csdn.net/qq_41228218/article/details/89715634

# 爬虫名称
BOT_NAME = 'Spider'

# 爬虫应用路径
SPIDER_MODULES = ['Spider.spiders']
NEWSPIDER_MODULE = 'Spider.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True
ROBOTSTXT_OBEY = False

# 并发请求数
CONCURRENT_REQUESTS = 2
# 单域名访问并发数，并且延迟下次秒数也应用在每个域名
CONCURRENT_REQUESTS_PER_DOMAIN  = 2
# 单IP访问并发数，如果有值则忽略：CONCURRENT_REQUESTS_PER_DOMAIN，并且延迟下次秒数也应用在每个IP
CONCURRENT_REQUESTS_PER_IP = 1
# 延迟下载秒数
DOWNLOAD_DELAY = 3

# 是否支持cookie, cookiejar进行操作cookie
COOKIES_ENABLED = False 
# COOKIES_DEBUG = True

# 爬虫允许的最大深度，可以通过meta查看当前深度；0表示无深度
# DEPTH_LIMIT = 3

# 16. 访问URL去重
# DUPEFILTER_CLASS = 'Spider.duplication.RepeatUrl'


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Spider Settings Start 爬虫级别配置

# >>>>>>>>>>>> Scfan Settings Start


# > 爬取盘搜搜 百度资源信息
LEVEL1_FILE = '/data/scrapy_data/baiduyun/level1.txt'
LEVEL2_FILE = '/data/scrapy_data/baiduyun/level2.txt'
LEVEL3_FILE = '/data/scrapy_data/baiduyun/level3.txt'
LEVEL4_FILE = '/data/scrapy_data/baiduyun/level4.txt'
RESULT_FILE = '/data/scrapy_data/baiduyun/result.txt'
# 百度网盘 资源存储
BAIDU_RESULT_FILE = '/data/scrapy_data/baiduyun/result.txt'

# 默认请求头
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'en',
}

# > 随机 User_Agent
USER_AGENT_LIST=[
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

# >>>>>>>>> 随机 IP 代理

# 代理文件名称
PROXY_FILE_NAME = "/data/scrapy_data/proxies.txt"
# 是否使用代理IP
IS_USE_PROXY = False
IS_USE_PROXY = True

# 是否处理 延迟加载
IS_USE_DELAY_LOAD_URL = False
IS_USE_DELAY_LOAD_URL = True
DELAY_LOAD_URL_TIME_first = 4
DELAY_LOAD_URL_TIME_second = 3

# >>>>>>>>> 添加文件
ITEM_PIPELINES = {
    'Spider.pipelines.SpiderPipeline': 300,
}
DOWNLOADER_MIDDLEWARES = {
    'Spider.middlewares.SpiderSpiderMiddleware': 1,
    #'proxySpider.middlewares.MyCustomDownloaderMiddleware': 543,


    # 随机 User_Agent
    'scrapy.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'Spider.randomAgentMiddleware.MyUserAgentMiddleware': 400,
    # scfan 代理IP - 参考链接: https://blog.csdn.net/Gooooa/article/details/74452203
    # Proxy后 含 延迟加载 页面功能
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware':None,  
    'Spider.middlewares.ProxyMiddleWare':125,  
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware':None,
    # Crawlera（专用于爬虫的代理组件），正确配置和设置下载中间件后，项目所有的request都是通过crawlera发出。
    # 'scrapy_crawlera.CrawleraMiddleware': 600
}

# CRAWLERA_ENABLED = True
# CRAWLERA_USER = '注册/购买的UserKey'
# CRAWLERA_PASS = '注册/购买的Password'


# >>>>>>>>>>>> Scfan Settings End





# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Spider.middlewares.SpiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'Spider.middlewares.SpiderDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'Spider.pipelines.SpiderPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
