import data_base as db
import matplotlib.pyplot as plt
import os


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


def each_month_num(conn,year):
    command = {}
    num_list = []
    price_list = []
    for month in range(1,13):
        m = "%02d" % month
        command[str(month)] = " select count(1),round(avg(unit_price),2) from chengjiao where sign_time >= '"+year+"."+m+".01' and sign_time <= '"+year+"."+m+".31' "
        num_list.append(db.run_commad(conn,command[str(month)])[0][0])
        price_list.append(db.run_commad(conn,command[str(month)])[0][1])
    print year
    print num_list
    draw_plot(num_list,'number_'+year,'b')
    print price_list
    draw_plot(price_list, 'avg_price_' + year,'r')


def draw_plot(data_list,ytitle,linecolor):
    fig = plt.figure()
    plt.plot(data_list, color = linecolor)
    plt.ylabel(ytitle)
    axes = plt.gca()
    axes.set_ylim([8000, 12000])
    axes.set_xlim([1, 12])
    if not os.path.exists('./image'):
        os.mkdir('./image')
    fig.savefig('./image/'+ytitle+'.png')



if __name__ == "__main__":
    conn = db.database_init()
    #each_year_num(conn)
    for year in range(2010,2018):
        each_month_num(conn, str(year))
