# -*- coding: utf-8 -*-

import urllib2
import random
import time
from bs4 import BeautifulSoup
import datetime
import Get_Cookies
import socket
import socks
import selenium.webdriver


def read_cookies():
    f = open("Cookies.txt", 'r')
    cookie_list = f.readlines()
    cookie_list = [u.strip() for u in cookie_list]
    f.close()
    return cookie_list


class myUrllib(object):
    cookies_last_update_time = datetime.datetime.now()
    #cookies_list = Get_Cookies.get_cookie_pool()
    cookies_list = read_cookies()
    interval_time = 7200
    SOCKS5_HOST = "127.0.0.1"
    SOCKS5_PORT = 1080
    default_socket = socket.socket
    socks.set_default_proxy(socks.SOCKS5, SOCKS5_HOST, SOCKS5_PORT)
    TIME_OUT = 10
    interval = [i for i in range(15, 45)]

    @classmethod
    def change_socket(cls):
        value = random.randint(1, 2)
        if value == 1:
            socket.socket = socks.socksocket
        elif value == 2:
            socket.socket = cls.default_socket

    @classmethod
    def update_time(cls):
        cur_time = datetime.datetime.now()
        print cls.cookies_last_update_time
        print cur_time
        temp = (cur_time - cls.cookies_last_update_time).seconds
        print temp
        if temp > cls.interval_time:
            socket.socket = cls.default_socket
            cls.cookies_list = Get_Cookies.get_cookie_pool()
            #cls.cookies_list = read_cookies()
            cls.cookies_last_update_time = datetime.datetime.now()
            for u in cls.cookies_list:
                print u

    @classmethod
    def get_page_webdriver(cls, url):
        '''
        调用浏览器下载页面
        '''
        try:
            socket.socket = cls.default_socket  # 浏览器不使用代理
            sleep_time = cls.interval[random.randint(0, len(cls.interval) - 1)]
            sleep_time = 0
            print u"sleep time : %d" % sleep_time
            time.sleep(sleep_time*2)
            driver = selenium.webdriver.Firefox()
            driver.get(url)
            source_code = driver.page_source
            plain_text = unicode(source_code)  # ,errors='ignore')
            soup = BeautifulSoup(plain_text, 'lxml')
            driver.quit()
            return soup
        except Exception, e:
            print e
            return None

    @classmethod
    def down_page(cls, url):
        cls.update_time()
        cls.change_socket()
        print socket.socket

        my_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            # 'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,en-US;q=0.2',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'cd.lianjia.com',
            'Upgrade-Insecure-Requests': '1',
            'Cookie': 'lianjia_uuid=35bd3c3f-b746-4977-aa52-136324c9414c; gr_user_id=64dbf94b-277a-4e83-8a61-e3961c03133c; UM_distinctid=15ad1b4858a47f-0728d079f310dd-57e1b3c-e1000-15ad1b4858b6d3; ubta=2299869246.2470332000.1489674777862.1489674777862.1489674777862.1; select_city=510100; all-lj=3e56656136803bc056cf7a329e54869e; Hm_lvt_660aa6a6cb0f1e8dd21b9a17f866726d=1490102667,1490102842,1490103459,1490156268; Hm_lpvt_660aa6a6cb0f1e8dd21b9a17f866726d=1490156268; gr_session_id_a1a50f141657a94e=083b1527-3f8d-4c86-811b-19c12274b58a; _smt_uid=58c923f9.332baf20; CNZZDATA1253492306=1192493743-1489571766-%7C1490152546; CNZZDATA1254525948=34400925-1489576498-%7C1490155475; CNZZDATA1255633284=2058035670-1489576264-%7C1490154092; CNZZDATA1255604082=1208633142-1489575094-%7C1490152933; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _ga=GA1.2.1699786726.1489576955; _gat_dianpu_agent=1; lianjia_ssid=7ff22987-1405-49e4-a210-a1da7ac841fa',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }

        sleep_time = cls.interval[random.randint(0, len(cls.interval)-1)]
        print u"sleep time : %d" % sleep_time
        time.sleep(sleep_time)
        #time.sleep(5)
        try:
            my_headers['Cookie'] = cls.cookies_list[random.randint(0, len(cls.cookies_list)-1)]
            req = urllib2.Request(url, headers=my_headers)
            source_code = urllib2.urlopen(req, timeout=cls.TIME_OUT).read()
            plain_text = unicode(source_code)  # ,errors='ignore')
            soup = BeautifulSoup(plain_text, 'lxml')
        except (urllib2.HTTPError, urllib2.URLError), e:
            print e
            return None
        except Exception, e:
            print e
            return None
        return soup
