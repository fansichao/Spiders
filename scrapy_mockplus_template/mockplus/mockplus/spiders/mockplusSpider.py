# -*- coding: utf-8 -*-
import scrapy
from mockplus.items import MockplusItem
import time
import os
import requests

# from AoiSolas.items import AoisolasItem

class mockpluspiderSpider(scrapy.Spider):
# class AoisolaspiderSpider(scrapy.Spider):
    name = "mockplus"
    allowed_domains = ["www.mockplus.cn"]
    start_urls = ['http://www.mockplus.cn/sample?page=%s'%i for i in range(1,13)]

    url_name_dic = {
"https://www.mockplus.cn/sample/post/1416":"音乐类原型设计分享 - Spotify",
"https://www.mockplus.cn/sample/post/1313":"交易类APP原型设计分享 - 5miles",
"https://www.mockplus.cn/sample/post/1312":"电影票APP原型设计分享– Movie Booking",
"https://www.mockplus.cn/sample/post/1311":"新闻类APP原型设计分享– Pinster",
"https://www.mockplus.cn/sample/post/1288":"文字创作类App分享-简书",
"https://www.mockplus.cn/sample/post/1287":"电商类APP原型设计分享– Koral",
"https://www.mockplus.cn/sample/post/1286":"修图类APP原型设计分享– Hello Camera",
"https://www.mockplus.cn/sample/post/1259":"摄影类APP原型设计分享– Nest Camera",
"https://www.mockplus.cn/sample/post/1256":"工具类APP原型设计分享 – NotePlan",
"https://www.mockplus.cn/sample/post/1245":"社交类APP原型设计分享 – Sparks Social",
"https://www.mockplus.cn/sample/post/1244":"旅行类app设计原型分享—Travelisto",
"https://www.mockplus.cn/sample/post/1243":"行程管理类APP原型设计分享 — Book your flight",
"https://www.mockplus.cn/sample/post/1242":"音乐类app设计原型分享—THE HOT 100",
"https://www.mockplus.cn/sample/post/697":"教育类App原型分享-Mimo",
"https://www.mockplus.cn/sample/post/696":"购物类App的原型制作分享-Villoid",
"https://www.mockplus.cn/sample/post/695":"Mockplus项目例子-IF（App，办公类）",
"https://www.mockplus.cn/sample/post/694":"Mockplus项目例子-支付宝9.9（App，财务类）",
"https://www.mockplus.cn/sample/post/693":"Mockplus项目例子-Timeglass（App，效率类）",
"https://www.mockplus.cn/sample/post/692":"Mockplus项目例子-ExpenseMobile（App，财务类）",
"https://www.mockplus.cn/sample/post/691":"Mockplus项目例子-Shopify（Web，电商类）",
"https://www.mockplus.cn/sample/post/690":"Mockplus项目例子-The Value Engineers（Web，企业类）",
"https://www.mockplus.cn/sample/post/689":"Mockplus项目例子-Asana Web（Web，工具类）",
"https://www.mockplus.cn/sample/post/688":"Mockplus项目例子-Chartistic（App，工具类）",
"https://www.mockplus.cn/sample/post/687":"Mockplus项目例子-Fedena（Web，软件类）",
"https://www.mockplus.cn/sample/post/686":"Mockplus项目例子-Globalsources（Web，电商类）",
"https://www.mockplus.cn/sample/post/685":"Mockplus项目例子-Ph.Oliviers（App，医疗类）",
"https://www.mockplus.cn/sample/post/1098":"官网类原型模板分享——Apple",
"https://www.mockplus.cn/sample/post/1095":"轻博客类Web原型制作分享——Tumblr",
"https://www.mockplus.cn/sample/post/1094":"社交类APP原型模板分享——Tinder",
"https://www.mockplus.cn/sample/post/1066":"社交类APP原型模板分享——微信",
"https://www.mockplus.cn/sample/post/1065":"电商类Web原型制作分享——天猫",
"https://www.mockplus.cn/sample/post/1052":"电商类web原型制作分享——美丽说",
"https://www.mockplus.cn/sample/post/1051":"电商类Web原型制作分享——聚美优品",
"https://www.mockplus.cn/sample/post/1050":"类Pinterest Web原型制作分享——花瓣网",
"https://www.mockplus.cn/sample/post/1047":"企业类Web原型制作分享-Kraftwerk",
"https://www.mockplus.cn/sample/post/1046":"电商类Web原型制作分享-IKEA",
"https://www.mockplus.cn/sample/post/1015":"奢侈品官网类Web原型制作分享-CHANEL",
"https://www.mockplus.cn/sample/post/959":"旅游类App的原型制作分享-Klook",
"https://www.mockplus.cn/sample/post/943":"健康类App原型制作分享-Mindmate",
"https://www.mockplus.cn/sample/post/710":"工具类App原型制作分享-Asana App",
"https://www.mockplus.cn/sample/post/709":"美食类App原型制作分享-Bon App！",
"https://www.mockplus.cn/sample/post/708":"健康类App原型制作分享-Pillow",
"https://www.mockplus.cn/sample/post/707":"旅游类App原型制作分享-Triposo",
"https://www.mockplus.cn/sample/post/706":"运动类App原型制作分享-Zombies, Run",
"https://www.mockplus.cn/sample/post/705":"微信原型组件分享-WeUI",
"https://www.mockplus.cn/sample/post/704":"音乐类App原型制作分享-Qello Concerts",
"https://www.mockplus.cn/sample/post/703":"旅游类App原型分享-Guides",
"https://www.mockplus.cn/sample/post/702":"体育新闻类原型分享-BBC Sport",
"https://www.mockplus.cn/sample/post/701":"健身类App原型分享-FitStar Yoga",
"https://www.mockplus.cn/sample/post/700":"健身工具类App原型分享-Coach.me",
"https://www.mockplus.cn/sample/post/699":"美食类APP原型分享-Feast",
"https://www.mockplus.cn/sample/post/698":"工具类App原型分享-Balanced",
"https://www.mockplus.cn/sample/post/739":"效率类App原型制作分享-Swipes",
"https://www.mockplus.cn/sample/post/738":"教育类App原型制作分享-Encode",
"https://www.mockplus.cn/sample/post/737":"美食类App原型制作分享-Beanhunter",
"https://www.mockplus.cn/sample/post/729":"工具类App原型制作分享-Workflow",
"https://www.mockplus.cn/sample/post/728":"服务类App原型制作分享-South Devon Accounting",
"https://www.mockplus.cn/sample/post/727":"工具类App原型制作分享-Pocket Fuel",
"https://www.mockplus.cn/sample/post/726":"体育类App原型制作分享-AusOpen",
"https://www.mockplus.cn/sample/post/725":"企业类Web原型制作分享-Valet",
"https://www.mockplus.cn/sample/post/723":"购物类App原型制作分享-Lyst",
"https://www.mockplus.cn/sample/post/722":"生活类App原型制作分享-AnyList",
"https://www.mockplus.cn/sample/post/713":"效率类App原型制作分享-One List",
"https://www.mockplus.cn/sample/post/712":"工具类App原型制作分享-Bear",
"https://www.mockplus.cn/sample/post/711":"美食类App原型制作分享-Recipes",
"https://www.mockplus.cn/sample/post/915":"工具类Web原型制作分享-Amcharts",
"https://www.mockplus.cn/sample/post/914":"饮品类App原型制作分享-WineRatingsPlus",
"https://www.mockplus.cn/sample/post/906":"图片素材类Web原型制作分享-Pexels",
"https://www.mockplus.cn/sample/post/905":"设计平台类Web原型制作分享-Dribbble",
"https://www.mockplus.cn/sample/post/904":"新闻类Web原型制作分享-BBC",
"https://www.mockplus.cn/sample/post/903":"工具类App原型制作分享-WizNote",
"https://www.mockplus.cn/sample/post/902":"设计社区类Web原型制作分享-Behance",
"https://www.mockplus.cn/sample/post/901":"设计工具类Web原型制作分享-Mockplus",
"https://www.mockplus.cn/sample/post/900":"工具类App原型制作分享-Explain Everything",
"https://www.mockplus.cn/sample/post/893":"教育类App原型制作分享-Busuu",
"https://www.mockplus.cn/sample/post/878":"照片类App原型制作分享-MoShow",
"https://www.mockplus.cn/sample/post/870":"阅读类App原型制作分享-Book Amigo",
"https://www.mockplus.cn/sample/post/862":"社交新闻类App原型制作分享-Weibo",
"https://www.mockplus.cn/sample/post/684":"Mockplus项目例子-China Daily（App，新闻类）",
"https://www.mockplus.cn/sample/post/683":"Mockplus项目例子-Farfetch（App，购物类）",
"https://www.mockplus.cn/sample/post/682":"Mockplus项目例子-Any.DO（App，效率类）",
"https://www.mockplus.cn/sample/post/681":"Mockplus项目例子-Lynda.com（App，教育类）",
"https://www.mockplus.cn/sample/post/680":"Mockplus项目例子-Product Hunt（Web，社区类）",
"https://www.mockplus.cn/sample/post/679":"Mockplus项目例子-So Stereo（Web，音乐类）",
"https://www.mockplus.cn/sample/post/678":"Mockplus项目例子-ShopStyle（App，购物类）",
"https://www.mockplus.cn/sample/post/677":"Mockplus项目例子-LIVE Score（App，体育类）",
"https://www.mockplus.cn/sample/post/676":"Mockplus项目例子-Fjuul（App，健身类）",
"https://www.mockplus.cn/sample/post/675":"Mockplus项目例子-Hours Keeper（App，工具类）",
"https://www.mockplus.cn/sample/post/674":"Mockplus项目例子-CERTUKLtd（App，天气类）",
"https://www.mockplus.cn/sample/post/673":"Mockplus项目例子-Secrets（App，工具类）",
"https://www.mockplus.cn/sample/post/672":"Mockplus项目例子-edX（Web，教育类）",
"https://www.mockplus.cn/sample/post/1185":"企业官网原型制作分享-Starbucks",
"https://www.mockplus.cn/sample/post/1183":"商业化博客平台原型制作分享-TypePad",
"https://www.mockplus.cn/sample/post/1168":"美食类Web原型制作分享-Taste",
"https://www.mockplus.cn/sample/post/1163":"工具类官网Web原型制作分享-Adobe",
"https://www.mockplus.cn/sample/post/1160":"软件工具类Web原型制作分享 - Sketch",
"https://www.mockplus.cn/sample/post/1157":"企业官网Web原型制作分享-Tesla",
"https://www.mockplus.cn/sample/post/1143":"旅游类的APP原型模板分享——Priceline",
"https://www.mockplus.cn/sample/post/1141":"服装类Web原型制作分享——Rodd & Gunn",
"https://www.mockplus.cn/sample/post/1126":"设计服务类网站原型模板分享——Fortyseven",
"https://www.mockplus.cn/sample/post/1124":"社交类APP原型模板分享——QQ",
"https://www.mockplus.cn/sample/post/1110":"室内设计类网站Web原型制作分享——Dinzd",
"https://www.mockplus.cn/sample/post/1106":"拼图类APP原型模板分享——简拼",
"https://www.mockplus.cn/sample/post/1102":"旅游类APP原型模板分享——爱彼迎",
"https://www.mockplus.cn/sample/post/843":"生活服务类App原型制作分享-Tide",
"https://www.mockplus.cn/sample/post/842":"运动健康类App原型制作分享-Steps",
"https://www.mockplus.cn/sample/post/841":"运动健康类App原型制作分享-Movesum",
"https://www.mockplus.cn/sample/post/832":"美图类App原型制作分享-Meitu",
"https://www.mockplus.cn/sample/post/831":"购物类App原型制作分享-Polyvore",
"https://www.mockplus.cn/sample/post/826":"饮品类App原型制作分享-Starbucks",
"https://www.mockplus.cn/sample/post/818":"求职类App原型制作分享-Part-time Clouds",
"https://www.mockplus.cn/sample/post/817":"社交类App原型制作分享-LinkedIn",
"https://www.mockplus.cn/sample/post/816":"阅读类App原型制作分享-Another Read",
"https://www.mockplus.cn/sample/post/807":"工具类App原型制作分享-TickTick",
"https://www.mockplus.cn/sample/post/806":"美食类App原型制作分享-Kitchen Stories",
"https://www.mockplus.cn/sample/post/796":"美食类App原型制作分享-Sooshi",
"https://www.mockplus.cn/sample/post/795":"交通类App原型制作分享-DiDi",
"https://www.mockplus.cn/sample/post/789":"天气类App原型制作分享-ColorfulClouds",
"https://www.mockplus.cn/sample/post/788":"视频类App原型制作分享-VUE",
"https://www.mockplus.cn/sample/post/787":"视频类App原型制作分享-PocketVideo",
"https://www.mockplus.cn/sample/post/774":"体育类App原型制作分享-Onefootball",
"https://www.mockplus.cn/sample/post/773":"日记类App原型制作分享-Grid Diary",
"https://www.mockplus.cn/sample/post/772":"旅游类App原型制作分享-Airbnb",
"https://www.mockplus.cn/sample/post/766":"学习类App原型制作分享-Wokabulary",
"https://www.mockplus.cn/sample/post/765":"健身类App原型制作分享-Pacer",
"https://www.mockplus.cn/sample/post/764":"记事类App原型制作分享-iBetter",
"https://www.mockplus.cn/sample/post/755":"生活管理类App原型制作分享-Way of Life",
"https://www.mockplus.cn/sample/post/754":"艺术类App原型制作分享-ArtStack",
"https://www.mockplus.cn/sample/post/753":"饮品类App原型制作分享-Smoothies",
"https://www.mockplus.cn/sample/post/740":"健康类App原型制作分享-Life Cycle",
"https://www.mockplus.cn/sample/post/658":"Mockplus项目例子-IMDb（App，娱乐类）",
"https://www.mockplus.cn/sample/post/656":"旅游类App的原型制作分享",
"https://www.mockplus.cn/sample/post/671":"Mockplus项目例子-携程旅行（小程序，旅游类）",
"https://www.mockplus.cn/sample/post/670":"Mockplus项目例子-小程序示例（小程序）",
"https://www.mockplus.cn/sample/post/669":"Mockplus项目例子-Houzz（App，生活类）",
"https://www.mockplus.cn/sample/post/668":"Mockplus项目例子-StyleXstyle（Web，时尚类）",
"https://www.mockplus.cn/sample/post/667":"Mockplus项目例子-easyJet（App，旅游类）",
"https://www.mockplus.cn/sample/post/666":"Mockplus项目例子-LINER（App，工具类）",
"https://www.mockplus.cn/sample/post/665":"Mockplus项目例子-Cradle（App，健康类）",
"https://www.mockplus.cn/sample/post/664":"Mockplus项目例子-Taskade（Web，工具类）",
"https://www.mockplus.cn/sample/post/663":"Mockplus项目例子-Musement（App，旅游类）",
"https://www.mockplus.cn/sample/post/662":"Mockplus项目例子-Noodler（App，美食类）",
"https://www.mockplus.cn/sample/post/661":"Mockplus项目例子-轻芒阅读（App，新闻类）",
"https://www.mockplus.cn/sample/post/660":"Mockplus项目例子-Basecamp（Web，管理类）",
"https://www.mockplus.cn/sample/post/659":"Mockplus项目例子-企业微信（App，工具类）",
    }
    
    start_urls = list(url_name_dic.keys())
                  
    def parse(self, response, fist_run=False):
        selector = scrapy.Selector(response)

        if fist_run:
            # <div class="contents">
            infos = selector.xpath('//div[@class="contents"]')

            for info in infos:
                # item = scrapy.JsuserItem()
                href = info.xpath('h4/a/@href').extract()
                title = info.xpath('h4/a/text()').extract()
                pro_url = 'http://www.mockplus.cn' + href[0]
                title = title[0]
                print('"%s":"%s",'%(pro_url, title))
        else:
            time.sleep(0.01)
            # <div id="post-content">
            infos = selector.xpath('//div[@id="post-content"]')

            print('>>>>>>>>>>'*20)
            print(len(self.url_name_dic))
            print(response.url)

            for info in infos:
                href = info.xpath('p/a/@href').extract()
                print(href)
                for h in href:
                    if '.zip' in h and 'mockplus.cn' in h:
                        cmd = 'wget %s -O "/data/scrapy_data/mockplus/%s.zip"  '%(h, self.url_name_dic.get(response.url))
                        print(">>>>>>>>>>>>>>>>> %s"%cmd)
                        os.system(cmd)
                    if 'pan' in h:
                        cmd = 'wget %s -O "/data/scrapy_data/mockplus/%s.zip"  '%(h, self.url_name_dic.get(response.url))
                        print(">>>>>>>>>>>>>>>>> %s"%cmd)
        


    def pro_parse(self, url):
        u""" 解析单个 项目原型
        """
        res = urllib.request.urlopen(url)
        print(res.read().decode("utf-8")) # 自己解码
        



        # list = 
        # list = response.css(".list-left dd:not(.page)")
        # for img in list:
        #     imgname = img.css("a::text").extract_first()
        #     imgurl = img.css("a::attr(href)").extract_first()
        #     imgurl2 = str(imgurl)
        #     print(imgurl2)
        #     next_url = response.css(".page-en:nth-last-child(2)::attr(href)").extract_first()
        #     if next_url is not None:
        #         # 下一页
        #         yield response.follow(next_url, callback=self.parse)

        #     yield scrapy.Request(imgurl2, callback=self.content)

    def content(self, response):
        item = MockplusItem()
        item['name'] = response.css(".content h5::text").extract_first()
        item['ImgUrl'] = response.css(".content-pic img::attr(src)").extract()
        yield item
        # 提取图片,存入文件夹
        # print(item['ImgUrl'])
        next_url = response.css(".page-ch:last-child::attr(href)").extract_first()

        if next_url is not None:
            # 下一页
            yield response.follow(next_url, callback=self.content)
