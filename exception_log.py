
# -*- coding: utf-8 -*-


def exception_write(fun_name, url):
    """
    写入异常信息到日志
    """
    f = open('log.txt', 'a')
    line = "%s-%s\n" % (fun_name, url)
    f.write(line)
    f.close()


def exception_xiaoqu(fun_name, url, url_house):
    f = open('xiaoqu_error.txt', 'a')
    line = "%s-%s-%s\n" % (fun_name, url, url_house)
    f.write(line)
    f.close()
