# coding: utf-8
import xlrd
import csv
import codecs
import os
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def s_data(a, st, w, y, z):
    y = y+1
    with codecs.open(f_name, 'a', 'gbk') as f:
        write = csv.writer(f)
        write.writerows([[a, st, w, y, z]])


def readxls(filename, var):  # xls和xlsx类文件检索
    data = xlrd.open_workbook(path+'\\'+filename)
    s_num = data.sheets()
    for s1 in range(0, len(s_num)):
        table = data.sheets()[s1]
        nrows = table.nrows
        ncols = table.ncols
        for i in range(0, nrows):
            for y in range(0, ncols):
                if var in str(table.row_values(i)[y]):
                    p1 = i+1
                    s_data(filename, s1+1, p1, y, var)


def readcsv(filename, var):  # csv类文件检索
    c_read = csv.reader(codecs.open(path+'\\'+filename, encoding='GBk'))
    k = 1
    for row in c_read:
        for a in range(0, len(row)):
            if var in row[a]:
                s_data(filename, 0, k, a, var)
        k += 1


def readtxt(filename, var):# txt类检索
    f = codecs.open(path + '\\'+filename, 'r', encoding='GBK')
    l = 1
    f.readlines()
    for line in f.readlines():
        if var in line:
            s_data(filename, 0, l, 0, var)
        l += 1


if __name__ == '__main__':
    d = raw_input('输入路径: '.encode("GBK")).decode('GBK')
    p = os.walk(d)
    inputchar = raw_input('关键词(查询多个以单空格间隔): '.encode("GBK")).decode('GBK')
    key_word = inputchar.split(' ')
    f_name = str(int(time.time())) + 'Search.csv'
    with codecs.open(f_name, 'w', 'gbk')as f1:
        t_write = csv.writer(f1)
        t_write.writerows([['文件名', '页数', '行数', '列数', '查询字']])
        f1.close()
    for s in p:
        path = s[0]
        print path
        for files in os.listdir(path):
            x = files
            print x
            for word in key_word:
                v = word
                if '.' in x:
                    x_type = x.split('.')[-1]
                    # print x
                    if x_type == 'xls' or x_type == 'xlsx':
                        readxls(x, v)
                    elif x_type == 'csv':
                        readcsv(x, v)
                    elif x_type == 'txt':
                        readtxt(x, v)
    print u'输出至文件名：' + f_name