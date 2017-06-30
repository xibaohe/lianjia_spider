# -*- coding: utf-8 -*-
import sys
import data_base as db
import constant as ct
import scrap_all_xiaoqu as sxq
import scrap_all_chenjiao as scj
import datetime
import time


def scrap_line(u):
    t = u.strip().split('-')
    if t[0] == 'chenjiao_page':
        bianhao = t[1][t[1].index('chengjiao/') + len('chengjiao/c'):-1]
        name = db.read_xiaoqu_name_by_bianhao(conn, bianhao)
        scj.xiaoqu_chengjiao_spider(conn, name, t[1], bianhao)
    elif t[0] == 'chengjiao_page_detail':
        bianhao = t[1][t[1].rindex('c') + 1:-1]
        scj.chengjiao_spider(conn, t[1], bianhao)
    elif t[0] == 'xiaoqu':
        sxq.xiaoqu_page_detail(conn, t[1])


def read_log(conn):
    '''
    补充log 中未爬的数据
    '''
    f = open('log.txt', 'r')
    lines = f.readlines()
    for u in lines:
        scrap_line(u)
    f.close()


def spider_all_xiaoqu(conn):
    for region in ct.regions_cd_pinyin:
        sxq.do_xiaoqu_spider(conn, region)


def spider_all_from_xiaoqu(conn):
    '''
    按小区爬取所有数据
    '''
    xiaoqu_list = db.read_all_xiaoqu(conn)
    f_count = 0
    for i in range(9183, len(xiaoqu_list)):
        u = xiaoqu_list[i]
        print "current is %d" % i
        result = scj.xiaoqu_chengjiao_spider(conn, u[0], u[3], u[5])
        if result is False:
            f_count += 1
            time.sleep(60*f_count*f_count)
        elif result is True:
            f_count = 0
        if f_count > 4:
            print "%d  network error!!!" % i
            print str(datetime.datetime.now())
            break


def read_xiaoqu_error(conn):
    f = open('xiaoqu_error.txt', 'r')
    lines = f.readlines()
    for u in lines:
        t = u.strip().split('-')
        print t[0]
        scj.chengjiao_detail_page(conn, t[2])
    f.close()


def spider_chengjiao_pages(conn):
    '''
    按照url:  http://cd.lianjia.com/chengjiao/pg100/  爬前页数
    '''
    f_count = 0
    for i in range(1, 101):
        url_page = u"http://cd.lianjia.com/chengjiao/pg%d/" % i
        result = scj.chengjiao_pages_spider(conn, url_page)
        print url_page
        if result is False:
            f_count += 1
            time.sleep(60 * f_count * f_count)
        elif result is True:
            f_count = 0
        if f_count > 4:
            print "%d  network error!!!" % i
            print str(datetime.datetime.now())
            break


def handle_xiaoqubianhao_is_null(conn):
    #处理成交记录中小区编号为0的情况
    cj_list = db.get_chengjiao_xiaoqubianhao_is_null(conn)
    for u in cj_list:
        print u[1]
        scj.chengjiao_detail_page(conn, u[1])


def handle_wenjiang_error(conn):
    cj_list = db.get_chengjiao_wenjiang_xiaoqu_error_(conn)
    for u in cj_list:
        print u[1]
        scj.chengjiao_detail_page(conn, u[1])


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")
    conn = db.database_init()
    #read_log(conn)
    #spider_chengjiao_pages(conn)
    #read_xiaoqu_error(conn)
    #handle_xiaoqubianhao_is_null(conn)
    handle_wenjiang_error(conn)


