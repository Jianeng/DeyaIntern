# -*- coding: utf-8 -*-

import datetime
import urllib
import urllib2
import cookielib
import re
from GetPageData import *



OilchemUrlBase = r"http://www.oilchem.net/"
OilchemUser = []
OilchemPass = []


def GetPP():
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
        url = r"http://plas.oilchem.net/330/208/318/"
        page = GetOneURLWithCookie(url, opener, True, data)


        # 3. Get Data
        today = datetime.datetime.now()
        today = today.strftime("%m月%d日")

        fname = "PP粉"+today+".txt"
        fp = open(fname.decode("utf8"), 'w')

        pattern1 = "(\d*-\d*元/吨)"
        pattern1 = re.compile(pattern1)

        datepattern = "发布时间：([\S]*)\s"
        datepattern = re.compile(datepattern)

        region = ["南京","临沂"]
        org = "(?:<li><a href=\")([.\S]*)\"\starget=\"_blank\"\stitle=\"\[PP粉\][.\S]*"
        for city in region:

            # Get the News Link
            pattern = org+city
            pattern = re.compile(pattern)
            match = re.findall(pattern, page)

            if (match == None):
               print "1:Nothing is found in the page, check the page format!"
               return None
            url = match[0]

            # Get the News Page
            newspage = GetOneURLWithCookie(url, opener, True)
            datematch = re.findall(datepattern, newspage)
            date = datematch[0]
            print unicode(city+"\t"+date,"utf-8")

            match1 = re.findall(pattern1, newspage)


            # Output Data
            fp.write(city+"\t"+date+"\n")

            if city=="南京":
                fp.write("当地主流价格: "+match1[0]+"\n\n")

            if city=="临沂":
                fp.write("市场主流价格: "+match1[0]+"\n")
                fp.write("山东地区主流出厂价格: "+ match1[1]+"\n\n")

        fp.close()
        print unicode("保存: "+fname,"utf-8")


        # 4. logout
        url = OilchemUrlBase + r"user/exit.shtml"
        GetOneURLWithCookie(url, opener, True)



    except urllib2.URLError as e:
        print "Get URL: " + url + " failed! Error is: " + str(e.reason)
        return None




