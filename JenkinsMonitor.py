# -*- coding:utf-8 -*-
#Author: Linco
import urllib2
import urllib
import time
import os
import traceback
import sys
from lxml import etree
reload(sys)
sys.setdefaultencoding('utf8')

def err_log_site(log):#  获取失败的log地址（log:地址对应readlines）
    log_site1 = ''
    k_wd = 'Log链接:'
    for line in log:
        if k_wd in line:

            log_site1 = line.split(k_wd)[-1]
    w = log_site1.strip()
    log_site = w.replace('\\', '/')
    return log_site #返回执行失败的地址字符串


def search_err_rows(s):  # 定位Task失败行(s为地址的readlines)
    l_t = 0
    key = 'Task执行失败'
    s_arrs = []
    for line2 in s:
        if key in line2:
            s_arrs.append(l_t)
        l_t += 1
    return s_arrs # 返回执行失败行的列表


def err_mess(l1, l2):  # 获取失败信息(l1:失败行列表， l2:地址对应readlines)
    error_l = []
    for rows in l1:
        lll = l2[rows-7:rows+1]
        erro = ''.join(lll)
        error_l.append(erro)
    return error_l      # 返回错误信息 列表


def img_link(num, y):#(num:任务id，y:地址)失败图片获取
    link_ = {'Name':'', 'Image_link':''}
    name_i = []
    link_i = []
    res = urllib2.urlopen(y)
    h_res = etree.HTML(res.read())
    img_links = h_res.xpath('/html/body/ul/li/a/@href')
    for s in img_links:
        if '_Fail' in s:
            x = y +'/'+s
            x1 = s.split('_')[-2]
            x2 = num+'_'+s.split('_')[-2]
            urllib.urlretrieve(x, 'D:/img/%s.png' % x2)
            name_i.append(x1)
            link_i.append(x)
    link_['Name'] = name_i
    link_['Image_link'] = link_i
    return link_


if __name__ == '__main__':
    p_dir = os.path.exists('D:\Img')
    if not p_dir:
        os.makedirs('D:\Img')
    compare1 = '失败'
    site_main = 'http://192.168.1.31:8080/job/test_sikuli_test/'
    # 'http://192.168.1.31:8080/job/test_sikuli_test/'
    # 'http://192.168.1.31:8080/job/auto_login_quanfu_run_single/'
    num = ''
    while True:
        try:
            response_main = urllib2.urlopen(site_main)
            html_main = etree.HTML(response_main.read())
            status_main = html_main.xpath('//*[@id="buildHistory"]/div[2]/table/tr[2]/td/div[1]/div/a/img/@tooltip')
            status = status_main[0].encode('unicode_escape').decode('string_escape')
            if compare1 in status:
                First_num = html_main.xpath('//*[@id="buildHistory"]/div[2]/table/tr[2]/td/div[1]/a/@href')
                trg = First_num[0].split('/')[-2]
                if num == trg:
                    pass

                else:
                    site_1 = site_main + trg + '/console'
                    response_1 = urllib2.urlopen(site_1)
                    E_log = response_1.readlines()
                    error_log_site = err_log_site(E_log)
                    site_2 = error_log_site + '/logger.txt'
                    error_logger = urllib2.urlopen(site_2).readlines()
                    search_E_R = search_err_rows(error_logger)
                    result_E = img_link(trg, error_log_site)
                    result_E['Message'] = err_mess(search_E_R, error_logger)
                    len_dir = len(result_E['Name'])
                    for s in range(0, len_dir):
                        print "Name:", result_E["Name"][s], '\n'
                        print "Message:\n", result_E['Message'][s].encode("GBK")
                        print 'Image_link:\n', result_E['Image_link'][s], '\n\n'
                    num = trg

            else:
                pass
            time.sleep(120)
        except :
            traceback.print_exc()
            time.sleep(120)



