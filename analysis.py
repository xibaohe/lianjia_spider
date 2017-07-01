# -*- coding: utf-8 -*-
import data_base as db
import matplotlib.pyplot as plt
import os
import constant as ct
plt.rcParams['font.sans-serif'] = ['SimHei']  #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  #用来正常显示负号


def each_year_num(conn):
    command = {}
    command['2010'] = " select count(1) from chengjiao where sign_time >= '2010.01.01' and sign_time <= '2010.12.31' "
    command['2011'] = " select count(1) from chengjiao where sign_time >= '2011.01.01' and sign_time <= '2011.12.31' "
    command['2012'] = " select count(1) from chengjiao where sign_time >= '2012.01.01' and sign_time <= '2012.12.31' "
    command['2013'] = " select count(1) from chengjiao where sign_time >= '2013.01.01' and sign_time <= '2013.12.31' "
    command['2014'] = " select count(1) from chengjiao where sign_time >= '2014.01.01' and sign_time <= '2014.12.31' "
    command['2015'] = " select count(1) from chengjiao where sign_time >= '2015.01.01' and sign_time <= '2015.12.31' "
    command['2016'] = " select count(1) from chengjiao where sign_time >= '2016.01.01' and sign_time <= '2016.12.31' "
    command['2017'] = " select count(1) from chengjiao where sign_time >= '2017.01.01' and sign_time <= '2017.12.31' "
    num_list = [0 for i in range(2010,2018)]
    i=0
    for year in range(2010,2018):
        num_list[i] = db.run_commad(conn,command[str(year)])[0][0]
        i=i+1
    print num_list


def each_month_num(conn,year,region='all'):
    command = {}
    num_list = []
    price_list = []
    for month in range(1,13):
        m = "%02d" % month
        if region == 'all':
            command[str(month)] = " select count(1),round(avg(unit_price),2) from chengjiao where sign_time >= '"\
                                  +year+"."+m+".01' and sign_time <= '"+year+"."+m+".31' "
        else:
            command[str(month)] = " select count(1),round(avg(unit_price),2) from chengjiao,xiaoqu " \
                                  " where chengjiao.xiaoqubianhao = xiaoqu.bianhao and xiaoqu.regionb='" + region + \
                                  "' and sign_time >= '"+year+"."+m+".01' and sign_time <= '"+year+"."+m+".31' "


        num_list.append(db.run_commad(conn,command[str(month)])[0][0])
        price_list.append(db.run_commad(conn,command[str(month)])[0][1])
    print year
    print num_list
    print price_list
    return num_list, price_list


def draw_plot_avg(data_list,ytitle,linecolor):
    x_len = len(data_list)
    fig = plt.figure()
    plt.plot(data_list, color = linecolor)
    plt.ylabel(ytitle)
    axes = plt.gca()
    axes.set_ylim(min(data_list)-100, max(data_list)+100)
    if x_len == 12:
        plt.xticks(range(0, x_len), ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
    else:
        plt.xticks(range(0, x_len),
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '1', '2', '3', '4', '5', '6'])
    if not os.path.exists('./image'):
        os.mkdir('./image')
    fig.savefig('./image/'+ytitle+'.png')


def draw_plot_number(data_list,ytitle):
    x_len = len(data_list)
    index = range(0,x_len)
    fig = plt.figure()
    plt.bar(index,data_list, alpha=0.5)
    plt.ylabel(ytitle)
    if x_len == 12:
        plt.xticks(range(0, x_len), ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
    else:
        plt.xticks(range(0, x_len),
                   ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '1', '2', '3', '4', '5', '6'])

    if not os.path.exists('./image'):
        os.mkdir('./image')
    fig.savefig('./image/'+ytitle+'.png')


def statistic(conn,region):
    data_2015 = each_month_num(conn, str(2015), region)
    data_2016 = each_month_num(conn, str(2016), region)
    data_2017 = each_month_num(conn, str(2017), region)
    data_2016_now = (data_2016[0] + data_2017[0][:6], data_2016[1] + data_2017[1][:6])
    draw_plot_number(data_2015[0], region+'_number_' + str(2015))
    draw_plot_avg(data_2015[1], region+'_avg_price_' + str(2015), 'r')
    draw_plot_number(data_2016_now[0], region+'_number_2016_now')
    draw_plot_avg(data_2016_now[1], region+'_avg_price_2016_now', 'r')




if __name__ == "__main__":
    conn = db.database_init()
    regions = []
    # statistic(conn, 'all')
    # for u in ct.regions_cd:
    #     print u
    #     statistic(conn, u)
    each_year_num(conn)


