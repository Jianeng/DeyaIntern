# -*- coding: utf-8 -*-

import cookielib
import datetime
import os
import re

from GetPageData import *

OilchemUrlBase = r"http://www.oilchem.net/"
OilchemUser = "rockyeah"
OilchemPass = "abc123"


# Get 隆众石化 page data
def GetPageLLDPE():
    try:
        # creat a cookie 
        # 声明一个CookieJar对象实例来保存cookie
        cookie = cookielib.CookieJar()
        # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
        handler = urllib2.HTTPCookieProcessor(cookie)
        # 通过handler来构建opener
        opener = urllib2.build_opener(handler)

        # 1. login
        url = OilchemUrlBase + r"user/userLogin.do?ajax=1&closewindow=&rnd=0.3240302528720349"
        # page POST parameter
        data = {}
        data["username"] = OilchemUser
        data["password"] = OilchemPass

        # do the login page
        page = GetOneURLWithCookie(url, opener, False, data)
        # 2. Get the Page data we want
        data = {}
        data["pName"] = "LLDPE"
        data["webFlag"] = "2"
        data["hndz"] = "0"
        url = r"http://price.oilchem.net/dmPrice/listProduct.lz?"
        page = GetOneURLWithCookie(url, opener, True, data)

        # 3. logout
        url = OilchemUrlBase + r"user/exit.shtml"
        GetOneURLWithCookie(url, opener, True)

        return page
    except urllib2.URLError as e:
        print "Get URL: " + url + " failed! Error is: " + str(e.reason)
        return None


# 打印表格数据
def PrintTable(header, data, info, region):
    fname = region + "Table.txt"
    fp = open(fname.decode("utf8"), 'w')

    # Print Header
    i = 0
    while (i < len(header)):
        fp.write(str(i) + "\t" + header[i] + "\n")
        i += 1

    # Print Data
    i = 0
    fp.write("\n" + r"#############################" + "\n\n")
    while (i < len(data)):
        fp.write(str(i) + "\t" + data[i] + "\n")
        i += 1
    fp.write("\n" + r"#############################" + "\n\n")

    # Print Info.
    i = 0
    while (i < len(info)):
        fp.write(str(i) + "\t" + info[i] + "\n")
        i += 1
    fp.close()


# 解析隆众石化页面中的价格
def GetDataLLDPE(page, region):

    # 找到表头
    pattern = r"(?:<table ){1}[\d\D]*?(?:" + region + r"){1}[\d\D]*?(?:</table>){1}"
    pattern = re.compile(pattern)
    match = re.search(pattern, page)
    if (match == None):
        print "1:Nothing is found in the page, check the page format!"
        return None

    # 得到数据表格位置
    index = match.end(0)

    # 获取数据表格
    pattern = r"(?:<table ){1}[\d\D]*?(?:</table>){1}"
    pattern = re.compile(pattern)
    match = re.search(pattern, page[index:])
    if (match == None):
        print "2:Nothing is found in the page, check the page format!"
        return None
    DataTable = match.group(0)

    # Header
    pattern1 = r"<strong>([\S]*)</strong>"
    # Data
    pattern2 = r"<td>\s*(?:\s|<span style='color:red'>)([0-9.%-]*)"
    # Info.
    pattern3 = '''blank">([.\S]*)</a>'''

    pattern1 = re.compile(pattern1, re.S)
    match1 = re.findall(pattern1, DataTable)

    pattern2 = re.compile(pattern2, re.S)
    match2 = re.findall(pattern2, DataTable)

    pattern3 = re.compile(pattern3, re.S)
    match3 = re.findall(pattern3, DataTable)

    if (match1 == None):
        print "3:Header not found in the Table, check the page format!"
        return None

    if (match2 == None):
        print "3:Data not found in the Table, check the page format!"
        return None

    if (match3 == None):
        print "3:Info. not found in the Table, check the page format!"
        return None

    # 统计表格行数
    num = 0
    for word in match3:
        if word == "LLDPE":
            num += 1

    # 保存到文本中

    # Date
    today = datetime.datetime.now()
    today = today.strftime("%m月%d日")

    # File name
    fname = region + "LLDPE价格 " + today + ".txt"

    # File Path
    path = os.getcwd()
    title = "LLDPE国内市场价"
    new_path = os.path.join(path, title)

    if not os.path.isdir(new_path):
        os.makedirs(new_path)
    os.chdir(new_path)

    # PrintTable(match1,match2,match3,region)

    # Output Data
    fp = open(fname.decode("utf8"), 'w')
    for t in range(num):
        fp.write("规格: " + match3[1 + 4 * t] + "\n")
        fp.write("生产企业：" + match3[2 + 4 * t] + "\n")
        fp.write("市场：" + match3[3 + 4 * t] + "\n\n")
        fp.write("日期\t\t主流价\t低端价\t高端价\t涨跌差\t涨跌率\n\n")
        i = 0
        while (i < 5):
            fp.write(match1[4 + i] + "\t\t" + match2[i * 3 + t * 17] + "\t" \
                     + match2[i * 3 + 1 + t * 17] + "\t" + match2[i * 3 + 2 + t * 17] + "\t")
            if i == 4:
                fp.write(match2[15 + t * 17] + "\t" + match2[16 + t * 17])
            fp.write("\n\n")
            i += 1
        fp.write("\n" + r"#############################" + "\n\n")

    print unicode("保存: " + fname, "utf-8")
    fp.close()
    os.chdir(path)


def GetLLDPE(regionlist=('华东地区', '华南地区', '华北地区', '华中地区', '东北地区', '西北地区', '西南地区')):
    page = GetPageLLDPE()
    for word in regionlist:
        GetDataLLDPE(page, word)
