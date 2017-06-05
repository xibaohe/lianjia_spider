
import selenium.webdriver
import urllib2
import socket
import socks
import sys

SOCKS5_HOST = "127.0.0.1"
SOCKS5_PORT = 1080



def down_page(url):

    my_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        # 'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,en-US;q=0.2',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'cd.lianjia.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
    interval = [i for i in range(30, 90)]
    try:
        req = urllib2.Request(url, headers=my_headers)
        source_code = urllib2.urlopen(req, timeout=20).read()
        plain_text = unicode(source_code)  # ,errors='ignore')
        print plain_text
    except (urllib2.HTTPError, urllib2.URLError), e:
        print e
        return None
    except Exception, e:
        print e
        return None


if __name__=="__main__":
    #driver = selenium.webdriver.Firefox()
    #driver.get("http://cd.lianjia.com")
    #driver.quit()


    reload(sys)
    sys.setdefaultencoding("utf-8")

    default_socket = socket.socket
    socks.set_default_proxy(socks.SOCKS5, SOCKS5_HOST, SOCKS5_PORT)
    socket.socket = socks.socksocket
    print socket.socket

    url = "http://icanhazip.com/"
    down_page(url)
    socket.socket = default_socket
    print socket.socket
    down_page(url)

