# -*- coding: utf-8 -*-
import urllib_wrapper as uw
import exception_log as el
import re
import data_base as db
import scrap_all_xiaoqu as sxq


def chengjiao_detail_page(db_cj, url_page):
    '''
    详细页
    http://cd.lianjia.com/chengjiao/106092880262.html
    '''
    soup = uw.myUrllib.get_page_webdriver(url_page)
    if soup is None:
        print "error: %s" % url_page
        return False
    div = soup.find('div', {'id': 'resblockCardContainer'})
    href = div.find('a', {'class': 'fr LOGCLICK'}).get('href')
    house_bianhao = re.findall(r'[0-9]+', url_page)[0]
    xiaoqubianhao = re.findall(r'[0-9]+', href)[0]
    xiaoquname = db.read_xiaoqu_name_by_bianhao(db_cj, xiaoqubianhao)
    if xiaoquname is not None:
        db.update_chengjiao(db_cj, xiaoqubianhao, house_bianhao)
    else:
        print '该小区不存在 %s' % xiaoqubianhao
        xiaoqu_url = 'http://cd.lianjia.com/xiaoqu/%s/' % xiaoqubianhao
        xiaoqu_dict = sxq.xiaoqu_page_detail(db_cj,xiaoqu_url)
        xiaoqu_chengjiao_spider(db_cj, xiaoqu_dict[u'小区名称'],xiaoqu_dict[u'成交链接'],xiaoqu_dict[u'编号'])


def chengjiao_spider(db_cj, url_page, xiaoqubianhao):
    """
    按小区 ，爬取页面链接中的成交记录  每一页上的详情
    """
    soup = uw.myUrllib.down_page(url_page)
    if soup is None:
        el.exception_write('chengjiao_page_detail', url_page)
        return False

    auth_type = soup.find('p', {'id': 'authType'})
    if auth_type:
        print u'链家网流量异常, 停止抓取 %s' % url_page
        el.exception_write('chengjiao_page_detail', url_page)
        return False
    #content = soup.find('div', {'class': 'page-box house-lst-page-box'})
    # total_pages = 0
    # if content:
    #     d = "d=" + content.get('page-data')
    #     exec (d)
    #     total_pages = d['totalPage']
    #
    # if total_pages == 0:
    #     print "detail is 0 page is %s" % url_page
    #     db.xiaoqu_chengjiao_done(db_cj, xiaoqubianhao)
    #     return True
    cj_list = soup.findAll('div', {'class': 'info'})
    for cj in cj_list:
        info_dict = {}
        title = cj.find("div", {"class": "title"})  # html
        if title == None:
            continue
        info_dict.update({u'房子名称': title.get_text().strip()})
        if title.a == None:
            continue
        url = title.a.get('href')
        if url == None:
            continue
        bianhao = re.findall(r'(\w*[0-9]+)\w*', url)

        info_dict.update({u'编号': bianhao[0]})
        info_dict.update({u'链接': url})
        info_dict.update({u'小区编号': xiaoqubianhao})

        dealDate = cj.find("div", {"class": "dealDate"})  # html
        if dealDate is None:
            info_dict.update({u'签约时间': ""})
        else:
            info_dict.update({u'签约时间': dealDate.get_text().strip()})

        cursor = db_cj.cursor()
        cursor.execute('select * from chengjiao where house_bianhao = (%s)', (bianhao[0],))
        values = cursor.fetchall()
        if len(values) != 0:
            print '%s is already scrapyed' % bianhao[0]
            continue

        print u"房子名称 %s %s" % (title.get_text().strip(), dealDate.get_text().strip())

        total_price = cj.find("div", {"class": "totalPrice"})  # html
        if total_price is None:
            info_dict.update({u'签约总价': ""})
        else:
            total_price1 = total_price.find("span", {"class": "number"})  # html
            if total_price1 is None:
                info_dict.update({u'签约总价': ""})
            else:
                info_dict.update({u'签约总价': total_price1.get_text().strip()})

        unit_price = cj.find("div", {"class": "unitPrice"})  # html
        if unit_price is None:
            info_dict.update({u'签约单价': ""})
        else:
            unit_price1 = unit_price.find("span", {"class": "number"})  # html
            if unit_price1 is None:
                info_dict.update({u'签约单价': ""})
            else:
                info_dict.update({u'签约单价': unit_price1.get_text().strip()})

        house_info = cj.find("div", {"class": "houseInfo"})  # html
        if house_info is None:
            info_dict.update({u'基本信息1':""})
        else:
            info_dict.update({u'基本信息1': house_info.get_text().strip()})

        position_info = cj.find("div", {"class": "positionInfo"})  # html
        if position_info is None:
            info_dict.update({u'基本信息2': " "})
        else:
            info_dict.update({u'基本信息2': position_info.get_text().strip()})

        deal_house_info = cj.find("div", {"class": "dealHouseInfo"})  # html
        if deal_house_info is None:
            info_dict.update({u'基本信息3': ""})
        else:
            info_dict.update({u'基本信息3': deal_house_info.get_text().strip()})

        deal_cycle_info = cj.find("div", {"class": "dealCycleeInfo"})  # html
        if deal_cycle_info is None:
            info_dict.update({u'基本信息4': ""})
        else:
            info_dict.update({u'基本信息4': deal_cycle_info.get_text().strip()})

        print u"编号 %s" % bianhao
        print u"房源URL %s" % url
        db.gen_chengjiao_insert_command(info_dict, db_cj)
    #db.xiaoqu_chengjiao_done(db_cj, xiaoqubianhao)
    return True


def chengjiao_pages_spider(db_cj, url_page):
    '''
    前100页
    '''
    soup = uw.myUrllib.down_page(url_page)
    if soup is None:
        el.exception_write('chengjiao_page_detail', url_page)
        return False

    auth_type = soup.find('p', {'id': 'authType'})
    if auth_type:
        print u'链家网流量异常, 停止抓取 %s' % url_page
        el.exception_write('chengjiao_page_detail', url_page)
        return False

    cj_list = soup.findAll('div', {'class': 'info'})
    for cj in cj_list:
        info_dict = {}
        title = cj.find("div", {"class": "title"})  # html
        if title == None:
            continue
        info_dict.update({u'房子名称': title.get_text().strip()})
        if title.a == None:
            continue
        url = title.a.get('href')
        if url == None:
            continue
        bianhao = re.findall(r'(\w*[0-9]+)\w*', url)
        xiaoqu_name = title.get_text().strip().split(" ", 1)[0]
        xiaoqubianhao = db.get_xiaoqubianhao_by_name(db_cj, xiaoqu_name)
        if xiaoqubianhao is None:
            xiaoqubianhao = ''
            print u'小区不存在或重复'
            el.exception_xiaoqu(xiaoqu_name, url_page, url)

        info_dict.update({u'编号': bianhao[0]})
        info_dict.update({u'链接': url})
        info_dict.update({u'小区编号': xiaoqubianhao})

        dealDate = cj.find("div", {"class": "dealDate"})  # html
        if dealDate is None:
            info_dict.update({u'签约时间': u"无"})
        else:
            info_dict.update({u'签约时间': dealDate.get_text().strip()})

        cursor = db_cj.cursor()
        cursor.execute('select * from chengjiao where house_bianhao = (%s)', (bianhao[0],))
        values = cursor.fetchall()
        if len(values) != 0:
            print '%s is already scrapyed' % bianhao[0]
            continue

        print u"房子名称 %s %s" % (title.get_text().strip(), dealDate.get_text().strip())

        total_price = cj.find("div", {"class": "totalPrice"})  # html
        if total_price is None:
            info_dict.update({u'签约总价': u"无"})
        else:
            total_price1 = total_price.find("span", {"class": "number"})  # html
            if total_price1 is None:
                info_dict.update({u'签约总价': u"无"})
            else:
                info_dict.update({u'签约总价': total_price1.get_text().strip()})

        unit_price = cj.find("div", {"class": "unitPrice"})  # html
        if unit_price is None:
            info_dict.update({u'签约单价': u"无"})
        else:
            unit_price1 = unit_price.find("span", {"class": "number"})  # html
            if unit_price1 is None:
                info_dict.update({u'签约单价': u"无"})
            else:
                info_dict.update({u'签约单价': unit_price1.get_text().strip()})

        house_info = cj.find("div", {"class": "houseInfo"})  # html
        if house_info is None:
            info_dict.update({u'基本信息1': u"无"})
        else:
            info_dict.update({u'基本信息1': house_info.get_text().strip()})

        position_info = cj.find("div", {"class": "positionInfo"})  # html
        if position_info is None:
            info_dict.update({u'基本信息2': u"无"})
        else:
            info_dict.update({u'基本信息2': position_info.get_text().strip()})

        deal_house_info = cj.find("div", {"class": "dealHouseInfo"})  # html
        if deal_house_info is None:
            info_dict.update({u'基本信息3': u"无"})
        else:
            info_dict.update({u'基本信息3': deal_house_info.get_text().strip()})

        deal_cycle_info = cj.find("div", {"class": "dealCycleeInfo"})  # html
        if deal_cycle_info is None:
            info_dict.update({u'基本信息4': u"无"})
        else:
            info_dict.update({u'基本信息4': deal_cycle_info.get_text().strip()})

        print u"编号 %s" % bianhao
        print u"房源URL %s" % url
        db.gen_chengjiao_insert_command(info_dict, db_cj)
    return True


def xiaoqu_chengjiao_spider(db_cj, xq_name, chengjiao_url, bianhao):
    """
    爬取小区成交记录   有多少页
    """
    soup = uw.myUrllib.down_page(chengjiao_url)
    if soup is None:
        print "chengjiao down error:"
        el.exception_write('chenjiao_page', chengjiao_url)
        return False

    content = soup.find('div', {'class': 'page-box house-lst-page-box'})
    total_pages = 0
    if content:
        d = "d=" + content.get('page-data')
        exec (d)
        total_pages = d['totalPage']
    print u'spidering %s-%s小区 %d' % (xq_name, chengjiao_url, total_pages)

    for i in range(total_pages):
        # 'http: // cd.lianjia.com / chengjiao / pg9c3011055393438 /'
        flag = 'chengjiao/'
        url_part1 = chengjiao_url[:chengjiao_url.find(flag) + len(flag)]
        url_part2 = chengjiao_url[chengjiao_url.find(flag) + len(flag):]
        mid = 'pg%d' % (i+1)
        url_page = url_part1 + mid + url_part2
        print url_page
        chengjiao_spider(db_cj, url_page, bianhao)

    return True

