#! -*- coding:utf-8 -*-
u"""

百度云盘 API

- 自动获取 指定关键字 资源
- 自动将资源存取到 百度云盘 中
- python2.7+ or python3.6+


上次测试日期: 2020-04-09


TODO 待实现功能
1. 部分参数被写死在代码中，虽然可以使用，后续情况未知
2. 百度云盘 提取码-验证码 功能



# Cookie样例 由于Cookie涉及账户信息，下面Cookie已修改，仅供参考

BAIDU_COOKIE="PANWEB=1; BAIDUID=923A5BDE1qwe647asd4E92C334192350D587E4:FG=1;
BIDUPSID=923A5BDE16474E92C334192qwe350D587E4;
PSTM=15813qwe13169;
BDCLND=htZZ6SMApcXvOZMqwe96rZqQcZxbosli4xpXyMhKgpx%2Fj0%3D;
MCITY=-179%3A; BDORZ=B490B5EqweBF6F3CD402E515D22BCDA1598;
recommendTime=guanjia2020-03-1qwe3%2016%3A15%3A00;
Hm_lvt_7a3960b6f067eb0085b7f96ff5qwee660b0=1584096155,1584101138,1584265339,1584267498;
delPer=0; PSINO=3; H_PS_PSSID=30975_14qwe69_21095_30794_30903_30824_31086;
Hm_lpvt_7a3960b6f067eqweb0085b7f96ff5e660b0=1584274302;
cflag=13%3A3;
BDUSS=DhldzR0TmRqwexRkp6ei1jeGc4LVYxOU94emNURDh5UWkzN1Z6RWhtVmdrbTZxSlZlSUFBQUFBJCQAAAAAAAAAAAEAAAAF
-~g5x6ezvunkwuQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALobbl66G25eT;
SCRC=d3f27690dd6c0a346qwed174483029754bb; STOKEN=40d692aa6b3ef7fa0qwe41cf0404c1466dd5cf45858323f48384296dd7f7c0736de;
PANPSC=2847981154796289755%3AbAgLjDNYqweOsBMAwFlu9uBTpgn1M6s6PFhX0h%2FHfAcgs%2BFZR9eKYGfrKqwe1M2R80bvszK9sKmG0jScwI2OVc1JRpeLM%2Fc5VTqAtBRNjpS2SKb1qcCNpWJnWVTkPbIrl
%2FMm6bcseJ9c69iCeQvaoB4mrv5XUvHO53SMyxqweMRmYrlFHgmqF9Kes%2FZQ%2FFe4PuTzNr1rr"


"""

# TODO Python 自动监测对象属性变化 从而执行函数 自动监听机制

import collections
import logging
import time
import requests
import os
import re
import copy
import traceback
import urllib
import json
import argparse
import sys

LOG_FILE = 'run.log'
LOG_FORMAT = "[%(asctime)s] %(name)s: [%(filename)s-%(lineno)d] %(levelname)-7s: %(message)s"
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S %a '
logging.basicConfig(
    # level=logging.INFO,
    level=logging.DEBUG,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    # filename 直接写入文件 不打印到控制台
    # filename=LOG_FILE
)

sh = logging.StreamHandler()  # 往屏幕上输出
sh.setFormatter(LOG_FORMAT)  # 设置屏幕上显示的格式
logging.getLogger(LOG_FILE).addHandler(sh)  # 把对象加到logger里

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
            'Connection': 'keep - alive',
        }

        self.init()
        # 有提取码的请求头 Cookie不同
        self.code_headers = copy.deepcopy(self.headers)

    def init(self, success_file=None, failed_file=None, isinit=False):
        u""" 初始化 参数等

        """
        self.success_file = success_file or 'file/success.txt'
        self.failed_file = failed_file or 'file/failed.txt'

        if isinit:
            os.remove(self.success_file)
            os.remove(self.failed_file)

        # 单个URL处理是否成功
        self.one_success = True
        self.one_msg = ''
        # 整体程序处理是否成功
        self.total_success = True
        self.total_msg = ''

        # 用户参数数据
        self.user_params_data = {
            # ondup存在且为newcopy时，无论文件是否存在都会保存
            'ondup': None,  # 'newcopy'
            'async': '1',
            'channel': 'chunlei',
            'web': '1',
            'clienttype': '0',
            # TODO logid无法从请求中获取，写死也可以用            
            'logid': 'MTU4NDA5NzUzNzc5ODAuMDIzODg1MzAyMzg4NzYwODU0',
            'bdstoken': 'null',
            # TODO 无法获取 写死也可以用
            'app_id': '250528',
        }

        # 读取的数据
        self.data = None

        # 已成功保存的文件 含成功保存和文件已存在的情况
        self.success_data = self._read_data(file_name=self.success_file)

        # 当前运行的 URL 信息
        self.url_dic = {};

        # 总计信息
        self.total_info = {
            # 文件条数
            'file_count': 0,
            # 有效条数
            'valid_count': 0,
            'success_count': 0,
            'failed_count': 0,
        }

    def _get_cookie(self):
        u""" 获取 cookie
        """
        # TODO cookie 暂不支持自动获取
        cookie = None
        return cookie

    def _check_class_status(self):
        u""" 检查类状态

        :return:
        """
        # TODO 实现类的自动监控 暂未使用
        if not self.total_success:
            raise ValueError(self.total_msg)

        if not self.one_success:
            logging.info('>>>> 单次运行错误，错误信息: \n%s' % self.one_msg)

    def _read_data(self, file_name=None):
        u""" 读取文件

        :param str file_name: 文件名称
        """
        logging.info('>>>> 读取文件[%s]' % file_name)
        data = []
        if not file_name or not os.path.exists(file_name):
            return data

        with open(file_name, "rb") as f:
            file_data = f.readlines()
            file_data = [str(a, encoding='utf-8').replace('\n', '') for a in file_data if a]

            for row in file_data:
                dic = dict()
                if not bool(row):
                    continue

                ll = row.strip().replace('\n', '').split(' ')
                ll = [i.strip() for i in ll if bool(i)]
                dic['url'] = ll[0]
                dic['code'] = ll[1] if len(ll) >= 2 else ''
                dic['type'] = 'have_code' if dic['code'] else 'not_code'
                data.append(dic)
        return data

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
        if not self.total_success:
            return

        data = list()

        if file_name:
            data = self._read_data(file_name=file_name)
            if not bool(data):
                raise ValueError('文件解析,数据为空,请检查文件数据!')
        elif url:
            ll = url.strip().replace('\n', '').split(' ')
            ll = [i.strip() for i in ll if bool(i)]
            dic['url'] = ll[0]
            dic['code'] = ll[1] if len(ll) >= 2 else ''
            dic['type'] = 'have_code' if dic['code'] else 'not_code'
            data.append(dic)
        else:
            raise ValueError('未输入数据!')

        # 非 http 开头的 url 自动去除
        self.data = [dic for dic in data if dic['url'].startswith('http') and dic not in self.success_data]
        # 去重 TODO 更优的写法
        tmp_data = list()
        for dic in self.data:
            if dic not in tmp_data:
                tmp_data.append(dic)
        self.data = copy.deepcopy(tmp_data)
        del tmp_data

        self.total_info['file_count'] = len(data)
        self.total_info['valid_count'] = len(self.data)
        return data

    def _one_failed(self, msg=None):
        u" 运行一次 失败 "
        self.one_msg = msg or self.one_msg
        self.one_success = False
        logging.error(self.one_msg)

    def _one_success(self, msg=None):
        u" 运行一次 成功 "
        self.one_msg = msg or self.one_msg
        self.one_success = True
        logging.info(self.one_msg)

    def save(self, save_path='/'):
        u""" 将资源 保存到 百度云盘中

        :param save_path: 百度云盘路径，默认根目录 /
        """
        if not bool(self.data):
            self.one_success = False
            self.one_msg = '未检测到数据,请先调用 read_data 读取数据!'
            raise ValueError('未检测到数据,请先调用 read_data 读取数据!')

        logging.info(">>>>>> URL Total Count [%s]" % (len(self.data)))
        for url_dic in self.data:
            self.url_dic = url_dic
            self.one_msg = ''
            self.one_success = True
            logging.info('>>>> Save Resource :\n%s' % url_dic)

            try:
                if url_dic['type'] == 'not_code':
                    self._save_getbody()
                    self._save_addziyuan(save_path)
                elif url_dic['type'] == 'have_code':
                    self.parse_code()
                    self._save_getbody()
                    self._save_addziyuan(save_path)
                else:
                    logging.info('Error: 资源[%s]类型错误,请检查!' % url_dic)
            except Exception as err:
                self._one_failed(msg=err)
                logging.error(traceback.format_exc())

            if not self.one_success:
                self._write_file(' '.join([self.url_dic['url'], self.url_dic['code']]), self.failed_file)
                self.total_info['failed_count'] += 1
            else:
                self._write_file(' '.join([self.url_dic['url'], self.url_dic['code']]), self.success_file)
                self.total_info['success_count'] += 1

        logging.info('总计信息: \n%s' % self.total_info)

    def parse_code(self):
        u""" 解析百度 提取码

        说明:
            1. surl 百度云盘 校验提取码参数之一
            exp:
                02 https://pan.baidu.com/s/1hfayjG35WldXn7LhPtdEwA
                01 https://pan.baidu.com/share/init?surl=hfayjG35WldXn7LhPtdEwA
        """
        if not self.one_success:
            return

        url = self.url_dic['url']
        code = self.url_dic['code']

        post_data = copy.deepcopy(self.user_params_data)

        if 'surl' in url:
            surl = url.split('surl')[-1]
        else:
            surl = url.split('/')[-1][1:]

        post_data.update(
            {
                'surl': surl,
                # TODO t 写死也可以用？
                't': '1585238556461',
            }
        )

        # post_url = "https://pan.baidu.com/share/verify?surl={surl}&t={t}&channel={channel}&web={web}&app_id={app_id}&bdstoken={bdstoken}&logid={logid}==&clienttype={clienttype}".format(**post_data)
        post_url = "https://pan.baidu.com/share/verify?surl={surl}&t={t}&channel={channel}&web={web}&bdstoken={bdstoken}&logid={logid}==&clienttype={clienttype}".format(**post_data)

        try:
            payload_data = {
                # 提取码
                'pwd': code,
                # 验证码 (部分资源需要验证码 验证码涉及图像识别 暂未实现) TODO
                'vcode': '',
                'vcode_str': '',
            }
            payload = "pwd={pwd}&vcode={vcode}&vcode_str={vcode_str}".format(**payload_data)
            payload = unquote(payload)
            if sys.version_info.major >= 3:
                payload = bytes(payload, encoding='utf-8')
            req = Request(url=post_url, data=payload, headers=self.headers)
            f = urlopen(req)
            result = json.loads(f.read())

            #            # 获取验证码
            #            infos = req.selector.xpath('//dl[@class="pickcode clearfix"]')
            #            print(infos
            #            for info in infos:
            #                vcodes = info.xpath('dd/img/@src').extract()
            #                print(vcodes)
            #            print(dir(req))

            if result["errno"] == 0:
                # 提取码 验证成功后 更新Cookie
                code_cookie = self.edit_cookie(self.cookie, {'BDCLND': result['randsk']})
                self.code_headers.update({'Cookie': code_cookie})
                self._one_success('提取码验证成功!')
            elif result["errno"] == -62:
                # TODO 需要识别验证码 需要图像识别 此处跳过此次识别
                # 等待一段时间后无需验证码时再次访问
                self._one_failed(msg='请输入验证码!,暂不支持验证码识别，跳过此次资源处理！')
            elif result["errno"] == -12:
                self._one_failed(msg='提取码错误！!')
            else:
                self._one_failed(msg='提取码验证失败!')

        except Exception as err:
            self._one_failed(msg=err)
            logging.error(traceback.format_exc())

    def edit_cookie(self, cookie='', edit_dic={}):
        u""" 根据kv 修改cookie部分内容

        :param str cookie: Cookie字符串 PSINO=3; BDORZ=Bxxxxx
        :param dict edit_dic: 修改字典 {'PSINO':10}

        :returns: Cookie
        """

        cookie_dic = collections.OrderedDict({row.split('=')[0]: row.split('=')[1] for row in cookie.split('; ')})

        if bool(edit_dic):
            cookie_dic.update({k: v for k, v in list(edit_dic.items()) if k in list(cookie_dic.keys())})

        return '; '.join(['%s=%s' % (k, v) for k, v in cookie_dic.items()])

    def _check_response_status(self, mode='check_content', content=None, request_result=None, error_infos=[]):
        u""" 检查请求后答复 状态

        说明:
            1. 通过 content 检验链接返回的数据是否正常
            2. 通过 request_result 校验请求结果是否正常
        """
        default_error_infos = ['分享的文件不存在', '链接错误没找到文件，请打开正确的分享链接!', '此链接分享内容可能因为涉及侵权、色情、反动、低俗等信息，无法访问！', '分享的文件已经被取消了', '你所访问的页面不存在了']
        error_infos = error_infos or default_error_infos

        for error_info in error_infos:
            if error_info in content:
                self._one_failed(msg=error_info)

    def _write_file(self, url_info, filename):
        u""" 文件写入

         url code
        """
        if url_info:
            cmd = "echo '%s' >> %s" % (url_info.strip(), filename)
            os.system(cmd)

    def _save_getbody(self):
        u""" 获取分享页面源码

        :param url: 资源链接
        """
        if not self.one_success:
            return

        url = self.url_dic['url']
        success = True
        data = dict()

        try:
            headers = self.code_headers if self.url_dic['type'] == 'have_code' else self.headers
            req = Request(url, headers=headers)
            file_obj = urlopen(req)
            content = file_obj.read()
            if sys.version_info.major >= 3:
                content = str(content, encoding='utf-8')

            self._check_response_status(content=content)
            if not self.one_success:
                return

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
            self._one_failed(msg=err)
            logging.error(traceback.format_exc())

        if not bool(data):
            self._one_failed(msg='未解析到HTML数据!')

        self.user_params_data.update(data)
        return {'success': success, 'data': data}

    def _save_addziyuan(self, save_path=None, user_params_data=None):
        u"""添加该资源到自己的网盘

        exp:
            sidlist=%5B1050206798214220%5D&path=%2Fscrapy_data
        """
        # TODO 无法保存自己分享的资源

        if not self.one_success:
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

        try:
            headers = self.code_headers if self.url_dic['type'] == 'have_code' else self.headers
            req = Request(url=post_url, data=payload, headers=headers)

            f = urlopen(req)

            result = json.loads(f.read())
            # logging.info("请求结果: %s" % result)
            if result["errno"] == 0:
                self._one_success(msg="[Save Resource] Success!")
            elif result["errno"] == 12:
                self._one_success(msg="[Save Resource] 资源已存在!")
            else:
                print(result)
                print(headers)
                self._one_failed(msg='[Save Resource] 异常报错!')

        except Exception as err:
            self._one_failed(msg='error')
            logging.error(traceback.format_exc())


COOKIE = os.environ.get('BAIDU_COOKIE', None)
SAVE_PATH = "/scrapy_data"
FILENAME = "resource.txt"
FILENAME = "file/badidu_result.txt"

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-filename', help="name of the file to process")
    parser.add_argument("-shareurl", help="add your shareurl")
    parser.add_argument("-path", help="add your baidupan-path")
    parser.add_argument("-cookie", help="add your baidupan-cookie")

    args = parser.parse_args()
    # print('>> 输出信息到日志文件[%s]' % LOG_FILE)

    if args.cookie:
        COOKIE = args.cookie or COOKIE
    else:
        # logging.info(parser.print_help())
        # exit(0)
        pass
    if args.path:
        SAVE_PATH = urllib.quote(args.path) or SAVE_PATH
    if args.shareurl:
        URL = args.shareurl or URL
    elif args.filename:
        FILENAME = args.filename or FILENAME
    else:
        # logging.info(parser.print_help())
        # exit(0)
        logging.warning('采用 代码预设值!')
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
