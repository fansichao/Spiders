#! -*- coding:utf-8 -*-
u"""

百度云盘 API

- 自动获取 指定关键字 资源
- 自动将资源存取到 百度云盘 中
- python2.7+ or python3.6+


上次测试日期: 2020-03-15

"""

import os
import re
import copy
import traceback
import urllib
import json
import argparse
import sys

if sys.version_info.major == 2:
    import urllib2
    from urllib2 import Request as Request
    from urllib2 import urlopen as urlopen
    from urllib import unquote as unquote
else:
    from urllib.request import Request as Request
    from urllib.request import urlopen as urlopen
    from urllib.request import unquote as unquote


class BaiduyunAPI(object):

    def __init__(self, cookie=None):

        self.cookie = self._get_cookie() or cookie

        self.headers = {
            'Host': "pan.baidu.com",
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cache-Control': 'max-age=0',
            # 'Referer':'https://pan.baidu.com/s/1kUOxT0V?errno=0&errmsg=Auth%20Login%20Sucess&&bduss=&ssnerror=0&',
            'Referer': 'https://pan.baidu.com/s/10W3hxtIdaPrxrx1QBHqqsQ?fid=73587813535044&errno=0&errmsg=Auth%20Login%20Sucess&&bduss=&ssnerror=0&traceid=',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'Cookie': self.cookie,
        }

        # 读取的数据
        self.data = None

        # 用户参数数据
        self.user_params_data = {}

        # 此次运行信息
        self.run_info_dic = {
            'data':[],
            'total_count': 0,
            'file_name': None,
            'error_count': 0,
            'success_count': 0,
            'total_time': 0,
        };

    def _get_cookie(self):
        u""" 获取 cookie
        """
        # TODO cookie 暂不支持自动获取
        cookie = None
        return cookie

    def get_resource(self):
        pass

    def read_data(self, file_name=None, url=None):
        u""" 读取文件
    
        :param str filename: 文件名称
        :param str url: url 或 url 提取码
    
        exp:
            filename:
                https://pan.baidu.com/s/1Y5C0gRS40aJdxVBrSSOrLg hm3u
                https://pan.baidu.com/s/10W3hxtIdaPrxrx1QBHqqsQ
            return:
                [
                    {'url':'https://pan.baidu.com/s/1Y5C0gRS40aJdxVBrSSOrLg', 'code':'hm3u', 'type':'have_code'},
                    {'url':'https://pan.baidu.com/s/10W3hxtIdaPrxrx1QBHqqsQ', 'code':None, 'type':'not_code'},
                ]
        """
        data = list()
        header = ['url', 'code', 'type']

        if file_name:
            if not file_name or not os.path.exists(file_name): 
                raise ValueError('文件[%s]不存在'%file_name)
    
            print('>>>> 读取文件[%s]'%file_name)
            with open(file_name, "rb") as f:
                file_data = f.readlines() 
                file_data = [str(a, encoding='utf-8').replace('\n','') for a in file_data if a]
                
                for row in file_data:
                    dic = dict()
                    if not bool(row):
                        continue

                    ll = row.strip().replace('\n','').split(' ')
                    ll = [i.strip() for i in ll if bool(i)]
                    dic['url'] = ll[0]
                    dic['code'] = ll[1] if len(ll) >= 2 else None
                    dic['type'] = 'have_code' if dic['code']  else 'not_code'
                    data.append(dic)
            if not bool(data):
                raise ValueError('文件解析,数据为空,请检查文件数据!')
        elif url:
            ll = url.strip().replace('\n','').split(' ')
            ll = [i.strip() for i in ll if bool(i)]
            dic['url'] = ll[0]
            dic['code'] = ll[1] if len(ll) >= 2 else None
            dic['type'] = 'have_code' if dic['code']  else 'not_code'
            data.append(dic)
        else:
            raise ValueError('未输入数据!')
        
        self.data = data
        return data

    def save(self, save_path='/'):
        u""" 将资源 保存到 百度云盘中

        """
        data = self.data

        if not bool(data):
            raise ValueError('未检测到数据,请先调用 read_data 读取数据!')

        print(">>>>>> URL Total Count [%s]" % (len(data)))
        for url_dic in data:
            print('>>>> Save Resource :\n%s' % url_dic)
            if url_dic['type'] == 'not_code':
                body_data = self._save_getbody(url_dic['url'])
                if body_data['success']:
                    self._save_addziyuan(save_path, body_data['data'])
            elif url_dic['type'] == 'have_code':
                # TODO 后续获取数据链接 无法获取输入验证码后信息
                if not self.user_params_data:
                   self._save_getbody(url_dic['url'])

                self.parse_code(url_dic)
                self._save_getbody(url_dic['url'] + '?errno=0&errmsg=Auth%20Login%20Sucess&&bduss=&ssnerror=0&traceid=')
                self._save_addziyuan(save_path)
            else:
                print('Error: 资源[%s]类型错误,请检查!'%url_dic)

    def parse_code(self, url_dic):
        u""" 解析百度 提取码

        说明:
            1. surl 百度云盘 校验提取码参数之一 
            exp:
                02 https://pan.baidu.com/s/1hfayjG35WldXn7LhPtdEwA
                01 https://pan.baidu.com/share/init?surl=hfayjG35WldXn7LhPtdEwA
        """
        url = url_dic['url']
        code = url_dic['code']

        if not self.user_params_data:
            print('未成功获取 用户参数数据!')
            return

        post_data = copy.deepcopy(self.user_params_data)   

        if 'surl' in url:
            surl = url.split('surl')[-1]
        else:
            surl = url.split('/')[-1][1:]

        post_data.update(
            {
                'surl': surl ,
                't':  '1585238556461',
            }
        )
        print(post_data)

        post_url = "https://pan.baidu.com/share/verify?surl={surl}&t={t}&channel={channel}&web={web}&app_id={app_id}&bdstoken={bdstoken}&logid={logid}==&clienttype={clienttype}".format(**post_data)

        try:
            payload = "pwd=%s&vcode=&vcode_str=" % code
            payload = unquote(payload)
            if sys.version_info.major >= 3:
                payload = bytes(payload, encoding='utf-8')
            req = Request(url=post_url, data=payload, headers=self.headers)
            print(dir(req.headers))
            self.cookie = req.headers['Cookie']
            self.headers.update({'Cookie': self.cookie})
        
            f = urlopen(req)
            
            result = json.loads(f.read())
            print(result)
            tag = result["errno"]
            if tag == 0 :
                print('Success 检验验证码成功!')
            elif tag == -62:
                print('Error 链接[%s] 提取码[%s] 错误!'%(url, code))
            else:
                print('Error 错误!')
            
        except Exception as err:
            print("[Error] ", str(err))
            print(traceback.format_exc())


    def _check_response_status(self, mode='check_content', content=None, request_result=None, error_infos=[]):
        u""" 检查请求后答复 状态

        说明:
            1. 通过 content 检验链接返回的数据是否正常
            2. 通过 request_result 校验请求结果是否正常
        """
        default_error_infos = ['分享的文件不存在', '链接错误没找到文件，请打开正确的分享链接!', '此链接分享内容可能因为涉及侵权、色情、反动、低俗等信息，无法访问！', '分享的文件已经被取消了', '你所访问的页面不存在了']
        error_infos = error_infos or default_error_infos


    def record_ready_runing_url(self):
        u""" 记录已经运行的 url

        """
        pass


    def _save_getbody(self, url):
        u""" 获取分享页面源码

        :param url: 资源链接
        """
        success = True
        data = dict()
        
        error_infos = ['分享的文件不存在', '链接错误没找到文件，请打开正确的分享链接!', '此链接分享内容可能因为涉及侵权、色情、反动、低俗等信息，无法访问！', '分享的文件已经被取消了']
        

        try:
            req = Request(url, headers=self.headers)
            file_obj = urlopen(req)
            content = file_obj.read()
            if sys.version_info.major >= 3:
                content = str(content, encoding='utf-8')

            for error_info in error_infos:     
                if error_info in content:
                    print(error_info)
                    return {'success': False, 'data':data, 'msg':error_info}

            # 正则，获取参数值
            re_gex = r'"app_id":"(\d*)".*"fs_id":(\d*).*"path":"([^"]*)".*"uk":(\d*).*"bdstoken":"(\w*)".*"shareid":(\d*)'
            re_complie = re.compile(re_gex)
            rows = re_complie.findall(content)

            if len(rows) > 0:
                data = {
                    'app_id': rows[0][0],
                    'fs_id': rows[0][1],
                    'path': rows[0][2],
                    'from': rows[0][3],
                    'bdstoken': rows[0][4],
                    'shareid': rows[0][5],
                }
        except Exception as err:
            print(traceback.format_exc())
            print("[Error]", str(err))


        if not bool(data):
            print('Error HTML解析失败 或 链接路径错误！')
            success = False

        # 添加其他默认参数
        data.update({
            # ondup存在且为newcopy时，无论文件是否存在都会保存
            'ondup': None,  # 'newcopy'
            'async': '1',
            'channel': 'chunlei',
            'web': '1',
            'clienttype': '0',
            # TODO logid无法从请求中获取，写死也可以用
            'logid': 'MTU4NDA5NzUzNzc5ODAuMDIzODg1MzAyMzg4NzYwODU0',
        })

        self.user_params_data = data
        return {'success': success, 'data':data}

    def _save_addziyuan(self, save_path=None, user_params_data=None):
        u"""添加该资源到自己的网盘

        exp:
            sidlist=%5B1050206798214220%5D&path=%2Fscrapy_data
        """
        # TODO 无法保存自己分享的资源

        if not self.user_params_data:
            print('未成功获取 用户参数数据!')
            return

        post_data = user_params_data or copy.deepcopy(self.user_params_data)

        post_data = {k: v for k, v in post_data.items() if v is not None}
        from_fs_id = post_data.pop('fs_id', None)

        if 'ondup' in post_data.keys():
            post_url = "https://pan.baidu.com/share/transfer?shareid={shareid}&from={from}&ondup={ondup}&async={async}&channel={channel}&web={web}&app_id={app_id}&bdstoken={bdstoken}&logid={logid}&clienttype=0".format(
                **post_data)
        else:
            post_url = "https://pan.baidu.com/share/transfer?shareid={shareid}&from={from}&async={async}&channel={channel}&web={web}&app_id={app_id}&bdstoken={bdstoken}&logid={logid}&clienttype=0".format(
                **post_data)

        payload = "fsidlist=[" + str(from_fs_id) + "]&path=" + save_path
        # http 转义
        payload = unquote(payload)
        if sys.version_info.major >= 3:
            payload = bytes(payload, encoding='utf-8')

        # print("[Info] Url_Post:", post_url)
        # print("[Info] payload:", payload)
        try:
            req = Request(url=post_url, data=payload, headers=self.headers)
            f = urlopen(req)
            
            result = json.loads(f.read())
            tag = result["errno"]
            # print("请求结果: %s" % result)
            if tag == 0:
                print("[Result] Add Success")
            elif tag == 12:
                print("[Result] Already Exist")
            else:
                print("[Result] Have Error")

        except Exception as err:
            print("[Error] ", str(err))
            print(traceback.format_exc())



COOKIE = "PANWEB=1; BAIDUID=923A5BDE16474E92C334192350D587E4:FG=1; BIDUPSID=923A5BDE16474E92C334192350D587E4; PSTM=1581313169; BDCLND=htZZ6SMApcXvOZM96rZqQcZxbosli4xpXyMhKgpx%2Fj0%3D; MCITY=-179%3A; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; recommendTime=guanjia2020-03-13%2016%3A15%3A00; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1584096155,1584101138,1584265339,1584267498; delPer=0; PSINO=3; H_PS_PSSID=30975_1469_21095_30794_30903_30824_31086; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1584274302; cflag=13%3A3; BDUSS=DhldzR0TmRxRkp6ei1jeGc4LVYxOU94emNURDh5UWkzN1Z6RWhtVmdrbTZxSlZlSUFBQUFBJCQAAAAAAAAAAAEAAAAF-~g5x6ezvunkwuQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALobbl66G25eT; SCRC=d3f27690dd6c0a346d174483029754bb; STOKEN=40d692aa6b3ef7fa041cf0404c1466dd5cf45858323f48384296dd7f7c0736de; PANPSC=2847981154796289755%3AbAgLjDNYOsBMAwFlu9uBTpgn1M6s6PFhX0h%2FHfAcgs%2BFZR9eKYGfrK1M2R80bvszK9sKmG0jScwI2OVc1JRpeLM%2Fc5VTqAtBRNjpS2SKb1qcCNpWJnWVTkPbIrl%2FMm6bcseJ9c69iCeQvaoB4mrv5XUvHO53SMyxMRmYrlFHgmqF9Kes%2FZQ%2FFe4PuTzNr1rr"
SAVE_PATH = "/scrapy_data"
FILENAME = "resource.txt"
FILENAME = "/data/scrapy_data/baiduyun/baidu_result.txt"
FILENAME = "/data/scrapy_data/baiduyun/level3.txt"



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-filename', help="name of the file to process")
    parser.add_argument("-shareurl", help="add your shareurl")
    parser.add_argument("-path", help="add your baidupan-path")
    parser.add_argument("-cookie", help="add your baidupan-cookie")

    args = parser.parse_args()

    print(parser.print_help())
    if args.cookie:
        COOKIE = args.cookie or COOKIE
    else:
        # print(parser.print_help())
        # exit(0)
        pass
    if args.path:
        SAVE_PATH = urllib.quote(args.path) or SAVE_PATH
    if args.shareurl:
        URL = args.shareurl or URL
    elif args.filename:
        FILENAME = args.filename or FILENAME
    else:
        # print(parser.print_help())
        # exit(0)
        print('采用 代码预设值!')
        pass


    BAIDUYUN = BaiduyunAPI(cookie=COOKIE)
    # 读取 URL 文件
    if FILENAME is not None:
        BAIDUYUN.read_data(file_name=FILENAME)
        BAIDUYUN.save(save_path=SAVE_PATH)
        
    else:
        # 读取 单个 URL
        BAIDUYUN.read_data(url=URL)
        BAIDUYUN.save(save_path=SAVE_PATH)
