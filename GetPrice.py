# -*- coding: utf-8 -*-

import cookielib
import datetime

from GetPageData import *
from TableFunction import *

# 1. 丙烯：华东地区及山东地区
# 2. LLDPE中国地区(前一天的数据)
# 3. LDPE中国地区(前一天的数据)
# 4. HDPE(注塑)中国地区(前一天的数据)
# 5. PP(均聚、共聚)中国地区(前一天的数据)
# 6. LLDPE价格(中油华北的大庆和吉林7042、中石化华北的齐鲁7042、中油华东的大庆7042、
# 中石化华东的扬子和镇海7042、中油华南的大庆和吉林7042、中石化华南的福建联合和茂名石化)
# 7. LDPE价格(中油华东的大庆2426H、中石化华东的茂名2426H)
# 8. PP价格(中油华北的大庆炼化T30S、中石化华北的济南和齐鲁、中油华东的大庆T30S、
# 中油华东的独山子K8003、中石化华东的九江和镇海T30S、中油华南的大庆和T30S、
# 中石化华南的福建联合和海南炼厂和茂名石化T30S)
# 9. PP粉料厂价(华北临沂)
# 10. LLDPE煤化工价(华北的陕西中煤7042)
# 11. BOPP价格(华东厚光膜江苏双良)
# 12. 临沂和南京粉料


# Login info.
OilchemUrlBase = r"http://www.oilchem.net/"
OilchemUser = "rockyeah"
OilchemPass = "abc123"

# Data URL
Dm = r"http://price.oilchem.net/dmPrice/listProduct.lz?"
Im = r"http://price.oilchem.net/imPrice/listProduct.lz?"
De = r"http://price.oilchem.net/depProList.lz?"
PP = r"http://plas.oilchem.net/330/208/318/"

# Date
today = datetime.datetime.now()
today = today.strftime("%m月%d日")

# File name
fname = today + "价格信息.txt"

#####################################################################################

# 声明一个CookieJar对象实例来保存cookie
cookie = cookielib.CookieJar()
# 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
handler = urllib2.HTTPCookieProcessor(cookie)
# 通过handler来构建opener
opener = urllib2.build_opener(handler)

# Page POST Parameter
LoginURL = OilchemUrlBase + r"user/userLogin.do?ajax=1&closewindow=&rnd=0.3240302528720349"
LoginData = {}
LoginData["username"] = OilchemUser
LoginData["password"] = OilchemPass

# Login
GetOneURLWithCookie(LoginURL, opener, False, LoginData)

# Get Data Page
Data = {}
# 丙烯：华东地区及山东地区
Data["pName"] = "丙烯"
Data["webFlag"] = "3"
Data["hndz"] = "0"
Page1 = GetOneURLWithCookie(Dm, opener, True, Data)

# LLDPE中国地区(前一天的数据)
Data["pName"] = "LLDPE"
Data["webFlag"] = "2"
Page2 = GetOneURLWithCookie(Im, opener, True, Data)

# LDPE中国地区(前一天的数据)
Data["pName"] = "LDPE"
Page3 = GetOneURLWithCookie(Im, opener, True, Data)

# HDPE(注塑)中国地区(前一天的数据)
Data["pName"] = "HDPE"
Page4 = GetOneURLWithCookie(Im, opener, True, Data)

# PP(均聚、共聚)中国地区(前一天的数据)
Data["pName"] = "PP粒"
Page5 = GetOneURLWithCookie(Im, opener, True, Data)

# LLDPE价格(中油华北的大庆和吉林7042、中石化华北的齐鲁7042、中油华东的大庆7042、
# 中石化华东的扬子和镇海7042、中油华南的大庆和吉林7042、中石化华南的福建联合和茂名石化)
Data["pName"] = "LLDPE"
Page6 = GetOneURLWithCookie(De, opener, True, Data)

# LDPE价格(中油华东的大庆2426H、中石化华东的茂名2426H)
Data["pName"] = "LDPE"
Page7 = GetOneURLWithCookie(De, opener, True, Data)

# PP价格(中油华北的大庆炼化T30S、中石化华北的济南和齐鲁、中油华东的大庆T30S、
# 中油华东的独山子K8003、中石化华东的九江和镇海T30S、中油华南的大庆和T30S、
# 中石化华南的福建联合和海南炼厂和茂名石化T30S)
Data["pName"] = "PP粒"
Page8 = GetOneURLWithCookie(De, opener, True, Data)

# PP粉料厂价(华北临沂)
Data["pName"] = "PP粉料"
Page9 = GetOneURLWithCookie(Dm, opener, True, Data)

# LLDPE煤化工价(华北的陕西中煤7042)
Data["pName"] = "LLDPE"
Page10 = GetOneURLWithCookie(Dm, opener, True, Data)

# BOPP价格(华东厚光膜江苏双良)
Data["pName"] = "BOPP"
Page11 = GetOneURLWithCookie(De, opener, True, Data)

# 临沂和南京粉料
Page12 = GetOneURLWithCookie(PP, opener, True, Data)

# Logout
LogoutURL = OilchemUrlBase + r"user/exit.shtml"
GetOneURLWithCookie(LogoutURL, opener, True)

#####################################################################################

fp = open(fname.decode("utf8"), 'w')

#####################################################################################

# 1.丙烯：华东地区及山东地区
region = ("华东地区", "山东地区")
for word in region:
    # 获取表格中的数据
    (Header, Data, Info) = FinTableData(word, Page1, 1)
    fname = "丙烯华东地区及山东地区" + "Table.txt"
    # PrintTable(Header, Data, Info, fname)
    # 输出表格
    RowNumber = Row(Info, "丙烯")
    WriteRow(fp, word, Header, 2, Data, 1, range(RowNumber), Info, 2, 1)

print "获取丙烯：华东地区及山东地区..."

# 2.LLDPE中国地区(前一天的数据)
# 获取表格中的数据
(Header, Data, Info) = FinTableData("中国地区", Page2, 2)
fname = "LLDPE中国地区(前一天的数据)" + "Table.txt"
# PrintTable(Header, Data, Info, fname)
# 输出表格
RowNumber = Row(Info, "LLDPE(丁烯基)")
WriteRow(fp, "中国地区", Header, 2, Data, 2, range(RowNumber), Info, 2, 1)

print "获取LLDPE中国地区(前一天的数据)..."

# 3.LDPE中国地区(前一天的数据)
# 获取表格中的数据
(Header, Data, Info) = FinTableData("中国地区", Page3, 2)
fname = "LDPE中国地区(前一天的数据)" + "Table.txt"
PrintTable(Header, Data, Info, fname)
# 输出表格
RowNumber = Row(Info, "LDPE(通用)")
WriteRow(fp, "中国地区", Header, 2, Data, 2, range(RowNumber), Info, 2, 1)

print "获取LDPE中国地区(前一天的数据)..."

# 4.HDPE(注塑)中国地区(前一天的数据)
(Header, Data, Info) = FinTableData("中国地区", Page4, 2)
fname = "HDPE(注塑)中国地区(前一天的数据)" + "Table.txt"
# PrintTable(Header, Data, Info, fname)
# 输出表格
Row = [2]
WriteRow(fp, "中国地区", Header, 2, Data, 2, Row, Info, 2, 1)

print "获取HDPE(注塑)中国地区(前一天的数据)..."

# 5.PP(均聚、共聚)中国地区(前一天的数据)
(Header, Data, Info) = FinTableData("中国地区", Page5, 2)
fname = "PP(均聚、共聚)中国地区(前一天的数据)" + "Table.txt"
# PrintTable(Header, Data, Info, fname)
# 输出表格
Row = [2, 3]
WriteRow(fp, "中国地区", Header, 2, Data, 2, Row, Info, 2, 1)

print "获取PP(均聚、共聚)中国地区(前一天的数据)..."

# 6.LLDPE价格(中油华北的大庆和吉林7042、中石化华北的齐鲁7042、中油华东的大庆7042、
# 中石化华东的扬子和镇海7042、中油华南的大庆和吉林7042、中石化华南的福建联合和茂名石化)
# 华北
(Header, Data, Info) = FinTableData("华北地区", Page6, 1)
fname = "LLDPE出厂价华北" + "Table.txt"
PrintTable(Header, Data, Info, fname)
# 输出表格
Row = [0, 2, 3]
WriteRow(fp, "华北地区", Header, 4, Data, 1, Row, Info, 4, 2)

# 华东
(Header, Data, Info) = FinTableData("华东地区", Page6, 1)
fname = "LLDPE出厂价华东" + "Table.txt"
PrintTable(Header, Data, Info, fname)
# 输出表格
Row = [0, 8, 9]
WriteRow(fp, "华东地区", Header, 4, Data, 1, Row, Info, 4, 2)

# 华南
(Header, Data, Info) = FinTableData("华南地区", Page6, 1)
fname = "LLDPE出厂价华南" + "Table.txt"
PrintTable(Header, Data, Info, fname)
# 输出表格
Row = [0, 2, 3, 6, 8, 9]
WriteRow(fp, "华南地区", Header, 4, Data, 1, Row, Info, 4, 2)

print "获取LLDPE企业出厂价..."

# 7.LDPE价格(中油华东的大庆2426H、中石化华东的茂名2426H)
(Header, Data, Info) = FinTableData("华东地区", Page7, 1)
fname = "LDPE华东" + "Table.txt"
# PrintTable(Header, Data, Info, fname)
# 输出表格
Row = [0, 3]
WriteRow(fp, "华东地区", Header, 4, Data, 1, Row, Info, 4, 2)

print "获取LDPE企业出厂价..."

# 8.PP价格(中油华北的大庆炼化T30S、中石化华北的济南和齐鲁、中油华东的大庆T30S、
# 中油华东的独山子K8003、中石化华东的九江和镇海T30S、中油华南的大庆和T30S、
# 中石化华南的福建联合和海南炼厂和茂名石化T30S)
# 华北
(Header, Data, Info) = FinTableData("华北地区", Page8, 1)
fname = "PP粒华北" + "Table.txt"
# PrintTable(Header, Data, Info, fname)
# 输出表格
Row = [4, 7, 8, 11, 12, 13, 14]
WriteRow(fp, "华北地区", Header, 4, Data, 1, Row, Info, 4, 2)

# 华东
(Header, Data, Info) = FinTableData("华东地区", Page8, 1)
fname = "PP粒华东" + "Table.txt"
# PrintTable(Header, Data, Info, fname)
# 输出表格
Row = [2, 3, 4, 29]
WriteRow(fp, "华东地区", Header, 4, Data, 1, Row, Info, 4, 2)

# 华南
(Header, Data, Info) = FinTableData("华南地区", Page8, 1)
fname = "PP粒华南" + "Table.txt"
# PrintTable(Header, Data, Info, fname)
# 输出表格
Row = [4, 7, 15, 22]
WriteRow(fp, "华南地区", Header, 4, Data, 1, Row, Info, 4, 2)

print "获取PP粒国内企业出厂价..."

# 9.PP粉料厂价(华北临沂)
(Header, Data, Info) = FinTableData("华北地区", Page9, 1)
fname = "PP粉料华北" + "Table.txt"
# PrintTable(Header, Data, Info, fname)
# 输出表格
Row = [0]
WriteRow(fp, "华北地区", Header, 4, Data, 1, Row, Info, 4, 1)

# 10.LLDPE煤化工价(华北的陕西中煤7042)
(Header, Data, Info) = FinTableData("华北地区", Page10, 1)
fname = "LLDPE市场价华北" + "Table.txt"
PrintTable(Header, Data, Info, fname)
# 输出表格
Row = [3]
WriteRow(fp, "华北地区", Header, 4, Data, 1, Row, Info, 4, 1)

print "获取PP粉料国内市场价..."

# 11.BOPP价格(华东厚光膜江苏双良)
# 华东
(Header, Data, Info) = FinTableData("华东地区", Page11, 1)
fname = "BOPP华东" + "Table.txt"
# PrintTable(Header, Data, Info, fname)
# 输出表格
Row = [8]
WriteRow(fp, "华东地区", Header, 4, Data, 1, Row, Info, 4, 2)

print "获取BOPP企业出厂价..."

#####################################################################################

fp.write("PP粉市场信息:\n\n")
# 临沂和南京粉料
# Data format
pattern1 = "(\d*-\d*元/吨)"
pattern1 = re.compile(pattern1)

datepattern = "发布时间：([\S]*)\s"
datepattern = re.compile(datepattern)

# Specify Citites
region = ["南京", "临沂"]
org = "(?:<li><a href=\")([.\S]*)\"\starget=\"_blank\"\stitle=\"\[PP粉\][.\S]*"

# Get Data for each City
for city in region:

    # Get the News Link
    pattern = org + city
    pattern = re.compile(pattern)
    match = re.findall(pattern, Page12)

    if (match == None):
        print "1:Nothing is found in the page, check the page format!"
    url = match[0]

    # Get the News Page
    newspage = GetOneURLWithCookie(url, opener, True)
    datematch = re.findall(datepattern, newspage)
    date = datematch[0]

    match1 = re.findall(pattern1, newspage)

    # Output Data
    fp.write(city + "\t" + date + "\n")

    if city == "南京":
        fp.write("当地主流价格: " + match1[0] + "\n\n")

    if city == "临沂":
        fp.write("市场主流价格: " + match1[0] + "\n")
        fp.write("山东地区主流出厂价格: " + match1[1] + "\n\n")

#####################################################################################

fp.close()
