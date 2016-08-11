# -*- coding: utf-8 -*-
import re


# 打印表格数据
def PrintTable(header, data, info, fname):
    fp = open(fname.decode("utf8"), 'w')

    # Print Header
    fp.write("Header: \n\n")
    i = 0
    while (i < len(header)):
        fp.write(str(i) + "\t" + header[i] + "\n")
        i += 1
    fp.write("\n" + r"#############################" + "\n\n")

    # Print Data
    i = 0
    fp.write("Data: \n\n")
    while (i < len(data)):
        fp.write(str(i) + "\t" + data[i] + "\n")
        i += 1
    fp.write("\n" + r"#############################" + "\n\n")

    # Print Info.
    i = 0
    fp.write("Info: \n\n")
    while (i < len(info)):
        fp.write(str(i) + "\t" + info[i] + "\n")
        i += 1
    fp.close()


# 匹配表格数据
def FinTableData(Region, Page, flag):
    # 匹配公式
    TablePattern1 = r"(?:<table ){1}[\d\D]*?(?:"
    TablePattern2 = r"){1}[\d\D]*?(?:</table>){1}"
    TablePattern3 = r"(?:<table ){1}[\d\D]*?(?:</table>){1}"

    HeaderPattern = r"<strong>([\S]*)</strong>"

    DataPattern = r">\s*(?!7042)([%|\-|0-9|.]+)\s*(?!</a>&nbsp)<"

    InfoPattern1 = '''blank">([.\S]*)</a>'''
    InfoPattern2 = '''blank">([^-0-9]*)</a>'''

    # 找到表头
    pattern = re.compile(TablePattern1 + Region + TablePattern2)
    match = re.search(pattern, Page)
    if (match == None):
        print "1:Table is found in the page, check the page format!"
        return None

    # 得到数据表格位置
    index = match.end(0)

    # 获取数据表格
    pattern = re.compile(TablePattern3)
    match = re.search(pattern, Page[index:])
    if (match == None):
        print "2:Table is found in the page, check the page format!"
        return None
    DataTable = match.group(0)

    # Header
    pattern1 = re.compile(HeaderPattern, re.S)
    HeaderMatch = re.findall(pattern1, DataTable)
    # Data
    pattern2 = re.compile(DataPattern, re.S)
    DataMatch = re.findall(pattern2, DataTable)
    # Info.
    if flag == 1:
        pattern3 = re.compile(InfoPattern1, re.S)
    if flag == 2:
        pattern3 = re.compile(InfoPattern2, re.S)

    InfoMatch = re.findall(pattern3, DataTable)

    if (HeaderMatch == None):
        print "3:Header not found in the Table, check the page format!"
        return None

    if (DataMatch == None):
        print "3:Data not found in the Table, check the page format!"
        return None

    if (InfoMatch == None):
        print "3:Info. not found in the Table, check the page format!"
        return None

    # fname = Region + "Table.txt"
    # PrintTable(HeaderMatch, DataMatch, InfoMatch, fname)

    return (HeaderMatch, DataMatch, InfoMatch)


# 统计表格行数
def Row(Info, word):
    num = 0
    for temp in Info:
        if temp == word:
            num += 1
    return num


# 输出表格中的某几行
def WriteRow(fp, Region, Header, HeaderStart, Data, RMB, Row, Info, InfoStep, Priceflag, InfoStart=0):
    if RMB == 1:
        if Priceflag == 1:
            DataStep = 3 * 5 + 2
        if Priceflag == 2:
            DataStep = 1 * 5 + 2
    if RMB == 2:
        if Priceflag == 1:
            DataStep = 3 * 5 + 3
        if Priceflag == 2:
            DataStep = 1 * 5 + 3

    if Priceflag == 1:
        for rn in Row:

            tempInfo = Info[(InfoStart + rn * InfoStep):(InfoStart + (rn + 1) * InfoStep)]
            fp.write(Region + ":" + ":".join(tempInfo) + "\n\n")

            fp.write("日期\t\t主流价\t低端价\t高端价\t涨跌差\t涨跌率\n\n")
            i = 0
            while (i < 5):
                fp.write(Header[HeaderStart + i] + "\t\t" + Data[rn * DataStep + i * 3] + "\t" \
                         + Data[rn * DataStep + i * 3 + 1] + "\t" + Data[rn * DataStep + i * 3 + 2] + "\t")
                if i == 4:
                    fp.write(Data[rn * DataStep + 15] + "\t" + Data[rn * DataStep + 16])
                fp.write("\t\n\n")
                i += 1

            fp.write("\n" + r"#############################" + "\n\n")

    if Priceflag == 2:
        for rn in Row:

            tempInfo = Info[(InfoStart + rn * InfoStep):(InfoStart + (rn + 1) * InfoStep)]
            fp.write(Region + ":" + ":".join(tempInfo) + "\n\n")

            fp.write("日期\t\t价格\t涨跌差\t涨跌率\n\n")
            i = 0
            while (i < 5):
                fp.write(Header[HeaderStart + i] + "\t\t" + Data[rn * DataStep + i] + "\t")
                if i == 4:
                    fp.write(Data[rn * DataStep + 5] + "\t" + Data[rn * DataStep + 6])
                fp.write("\t\n\n")
                i += 1

            fp.write("\n" + r"#############################" + "\n\n")
