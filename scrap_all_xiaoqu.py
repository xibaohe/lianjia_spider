# -*- coding: utf-8 -*-
import urllib_wrapper as uw
import data_base as db
import constant as ct
import re
import exception_log as el
import sys


def xiaoqu_page_detail(db_xq, url_page='http://cd.lianjia.com/xiaoqu/3011056075583/'):
    soup = uw.myUrllib.down_page(url_page)
    if soup is None:
        el.exception_write("xiaoqu",url_page)
        return None
    xiaoqu_info = soup.find('div', {'class': 'fl l-txt'})
    all_a = xiaoqu_info.findAll('a')
    regionb = all_a[2].text[0:-2]
    regions = all_a[3].text[0:-2]
    xiaoqu_name = all_a[4].text
    url = soup.find('div', {'id': 'frameDeal'})
    chengjiaolink = url.find('a', {'class': 'btn-large'}).get('href')

    info_dict = {}
    info_dict.update({u'小区名称': xiaoqu_name})
    info_dict.update({u'编号': re.findall(r'[0-9]+', url_page)[0]})
    info_dict.update({u'成交链接': chengjiaolink})
    info_dict.update({u'大区域': regionb})
    info_dict.update({u'小区域': regions})
    db.gen_xiaoqu_insert_command(info_dict, db_xq)
    return info_dict


def xiaoqu_spider(db_xq, url_page):
    """
    爬取页面链接中的小区信息
    """
    soup = uw.down_page(url_page)
    if soup is None:
        print "soup none error"
        print url_page
        return
    xiaoqu_list = soup.findAll('div', {'class': 'info'})
    for xq in xiaoqu_list:
        info_dict = {}
        housetitle = xq.find("div", {"class": "title"})  # html
        print u"小区名称 %s" % housetitle.get_text().strip()
        info_dict.update({u'小区名称': housetitle.get_text().strip()})
        url = housetitle.a.get('href');
        bianhao = re.findall(r'(\w*[0-9]+)\w*', url)
        print u"编号 %s" % bianhao
        info_dict.update({u'编号': bianhao[0]})

        houseinfo = xq.find("div", {"class": "houseInfo"})  # html
        info_dict.update({u'成交链接': houseinfo.a.get('href')})

        print u"位置 %s" % xq.find('a', {'class': 'district'}).text
        info_dict.update({u'大区域': xq.find('a', {'class': 'district'}).text})
        info_dict.update({u'小区域': xq.find('a', {'class': 'bizcircle'}).text})
        db.gen_xiaoqu_insert_command(info_dict, db_xq)


def do_xiaoqu_spider(db_xq, region):
    """
    爬取大区域中的所有小区信息
    """
    second_path = u"xiaoqu/"
    url = ct.base_url + second_path + region + "/"
    print url

    soup = uw.down_page(url)
    if soup is None:
        return

    d = "d=" + soup.find('div', {'class': 'page-box house-lst-page-box'}).get('page-data')
    exec (d)
    total_pages = d['totalPage']
    print total_pages

    urls = []
    for i in range(total_pages):
        urls.append(ct.base_url + second_path + region + "/pg%d/" % (i + 1))

    # if region == 'gaoxin7':
    #     urls = urls[7:]
    for u in urls:
        print u
        xiaoqu_spider(db_xq, u)
    print u"爬下了 %s 区全部的小区信息" % region


# if __name__ == '__main__':
#     reload(sys)
#     sys.setdefaultencoding("utf-8")
#     xiaoqu_page_detail()