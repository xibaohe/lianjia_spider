# -*- coding: utf-8 -*-
import time
import selenium.webdriver
import random
import sched
import time
import datetime

cookie_interval_time = 7200


def gen_cookiestr(dict):
    cookie_str = ''
    for k, v in dict.items():
        cookie_str += k
        cookie_str += '='
        cookie_str += v
        cookie_str += '; '
    cookie_str = cookie_str[:-2]
    return cookie_str


def get_cookie():
    driver = selenium.webdriver.Firefox()
    try:
        driver.get("http://cd.lianjia.com")
        cookie = driver.get_cookies()
        cookie_dict = {}
        for u in cookie:
            if 'lianjia.com' in u['domain']:
                cookie_dict[u['name']] = u['value']
        print cookie_dict
        print len(cookie_dict)

        driver.quit()
        return gen_cookiestr(cookie_dict)
    except Exception, e:
        print e
        return None


def get_cookie_pool(n=5):
    f = open("Cookies.txt" ,'w')
    interval = [i for i in range(15, 45)]
    cookie_pool = []
    for i in range(n):
        time.sleep(interval[random.randint(0, len(interval) - 1)])
        str = get_cookie()
        if str is not None:
            cookie_pool.append(str)
            f.write(str + '\n')
    f.close()
    return cookie_pool


#
# def sche_job(s):
#     print str(datetime.datetime.now())
#     get_cookie_pool(5)
#     s.enter(cookie_interval_time, 1, sche_job, (s,))


# if __name__ == "__main__":
#     get_cookie_pool(5)
#     s = sched.scheduler(time.time, time.sleep)
#     s.enter(cookie_interval_time, 1, sche_job, (s,))
#     s.run()



