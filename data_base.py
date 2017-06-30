# -*- coding: utf-8 -*-
import mysql.connector


def read_all_xiaoqu(conn):
    cursor = conn.cursor()
    cursor.execute('select * from xiaoqu order by bianhao desc ')
    xq_list = cursor.fetchall()
    return xq_list


def get_xiaoqubianhao_by_name(conn,name):
    cursor = conn.cursor()
    #command = 'select bianhao from xiaoqu where name = (%s)' % name
    cursor.execute('select bianhao from xiaoqu where name = (%s)', (name, ))
    xq_bianhao = cursor.fetchall()
    if len(xq_bianhao) == 1:
        return xq_bianhao[0][0]
    elif len(xq_bianhao) == 0:
        return None
    else:
        print u"duplicated  小区名字u %s" % name
        return None


def read_xiaoqu_name_by_bianhao(conn,bianhao):
    cursor = conn.cursor()
    command = 'select name from xiaoqu where bianhao = (%s)' % bianhao
    cursor.execute(command)
    xq_name = cursor.fetchall()
    if len(xq_name) == 1:
        return xq_name[0]
    else:
        return None


def get_all_chengjiao_orderby_time(conn):
    cursor = conn.cursor()
    cursor.execute(" select * from chengjiao order by sign_time ")
    all_list = cursor.fetchall()
    return all_list


def run_commad(conn,commad):
    cursor = conn.cursor()
    cursor.execute(commad)
    return cursor.fetchall()


def get_chengjiao_xiaoqubianhao_is_null(conn):
    cursor = conn.cursor()
    cursor.execute(" select * from chengjiao where xiaoqubianhao = '' ")
    cj_list = cursor.fetchall()
    return cj_list

def get_chengjiao_wenjiang_xiaoqu_error_(conn):
    cursor = conn.cursor()
    cursor.execute(" select * from chengjiao where xiaoqubianhao = 1620020495512202 order by sign_time")
    cj_list = cursor.fetchall()
    return cj_list




def update_chengjiao(db_cj,xiaoqubianhao,house_bianhao):
    cursor = db_cj.cursor()
    cursor.execute("update chengjiao set xiaoqubianhao = (%s) where house_bianhao = (%s)", (xiaoqubianhao, house_bianhao))
    db_cj.commit()
    cursor.close()


def xiaoqu_chengjiao_done(db_cj, bianhao):
    '''
    小区是否已经爬完
    '''
    cursor = db_cj.cursor()
    cursor.execute("update xiaoqu set baseinfo = '0' where bianhao = (%s)", (bianhao,))
    db_cj.commit()
    cursor.close()


def gen_xiaoqu_insert_command(info_dict, conn):
    """
    生成小区数据库插入命令
    """
    info_list = [u'小区名称', u'大区域', u'小区域', u'成交链接', u'基本信息', u'编号']
    t = []
    for il in info_list:
        if il in info_dict:
            t.append(info_dict[il])
        else:
            t.append('')
    t = tuple(t)

    cursor = conn.cursor()
    cursor.execute('select * from xiaoqu where bianhao = (%s)', (info_dict[u'编号'],))
    values = cursor.fetchall()
    if len(values) == 0:
        command = "insert into xiaoqu (name,regionb,regions,chengjiaolink,baseinfo,bianhao) " \
                  "values ('%s','%s','%s','%s','%s','%s')" % t
        print command
        cursor.execute(command)
        conn.commit()
    cursor.close()


def gen_chengjiao_insert_command(info_dict, conn):
    """
    生成成交记录数据库插入命令
    """
    info_list = [u'编号', u'链接', u'房子名称', u'签约时间', u'签约单价', u'签约总价', u'基本信息1', u'基本信息2', u'基本信息3',u'基本信息4', u'小区编号' ]
    t = []
    for il in info_list:
        if il in info_dict:
            t.append(info_dict[il])
        else:
            t.append('')
    t = tuple(t)
    cursor = conn.cursor()
    cursor.execute('select * from chengjiao where house_bianhao = (%s)', (info_dict[u'编号'],))
    values = cursor.fetchall()
    if len(values) == 0:
        command = "insert into chengjiao (" \
                  "house_bianhao," \
                  "href," \
                  "housename," \
                  "sign_time," \
                  "unit_price," \
                  "total_price," \
                  "info1," \
                  "info2," \
                  "info3," \
                  "info4," \
                  "xiaoqubianhao" \
                  ") values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % t
    else:
        print u"house_bianhao already exists!! %s" % info_dict[u'编号']
    print command
    cursor.execute(command)
    conn.commit()
    cursor.close()


def database_init():
    conn = mysql.connector.connect(user='root', password='123456', database='house_cd', host='localhost')
    dbc = conn.cursor()

    dbc.execute(
        "create table if not exists xiaoqu ("
        "name varchar(200) ," +
        "regionb varchar(200), " +
        "regions varchar(200), " +
        "chengjiaolink varchar(200), "   +
        "baseinfo varchar(200)," +
        "bianhao varchar(45) primary key UNIQUE" +
        ")")

    dbc.execute(
        "create table if not exists chengjiao (" +
        "house_bianhao varchar(200) primary key UNIQUE, " +
        "href varchar(200)," +
        "housename varchar(200), " +
        "sign_time varchar(45), " +
        "unit_price varchar(45), " +
        "total_price varchar(45), " +
        "info1 varchar(200), " +
        "info2 varchar(200), " +
        "info3 varchar(200), " +
        "info4 varchar(200), " +
        "xiaoqubianhao varchar(45) )"
    )

    conn.commit()
    dbc.close()
    return conn
