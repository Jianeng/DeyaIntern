# -*- coding: utf-8 -*-
import re


# 打印表格数据
def PrintTable(header, data, info, fname):
    # 输入表格的Header表头(第一行)、Data价格信息(数据)、Info产品信息(规格、厂商等)、文件名
    # 以上参数除文件名外,由FindTableData函数获得
    # 新建包含以上信息的txt文件,用于寻找数据位置及查错


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


# 获取表格数据
def FindTableData(Region, Page, flag):
    # 输入地区、网页
    # flag=1: 国内价格(数据无超链接)
    # flag=2: 国际价格(数据有超链接)
    # 输出表格的Header表头(第一行)、Data价格信息(数据)、Info产品信息(规格、厂商等)

    # 匹配公式
    # 表格
    TablePattern1 = r"(?:<table ){1}[\d\D]*?(?:"
    TablePattern2 = r"){1}[\d\D]*?(?:</table>){1}"
    TablePattern3 = r"(?:<table ){1}[\d\D]*?(?:</table>){1}"

    # 表头
    HeaderPattern = r"<strong>([\S]*)</strong>"

    # 价格信息
    DataPattern = r">\s*(?!7042)([%|\-|0-9|.]+)\s*(?!</a>&nbsp)<"

    # 产品信息
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
    # 输入表格的Info(由FindTableData函数获得)和产品名称(如"LLDPE"等出现在表格第一列中的名称)
    # 输出表格行数(不包括表头)
    num = 0
    for temp in Info:
        if temp == word:
            num += 1
    return num


# 输出表格中的某几行
def WriteRow(fp, Region, Header, HeaderStart, Data, RMB, Row, Info, InfoStep, Priceflag):
    # fp: txt文件
    # Region: 地区名称
    # Header: 表头(由FindTableData函数获得)
    # HeaderStart: 第一个日期在表头中的位置
    # Data: 价格(由FindTableData函数获得)
    # RMB: 国内价格 RMB=1; 国际价格(表格中有人民币价格) RMB=2
    # ROW: 需要写入txt的行(从0开始计数)
    # Info: 产品信息(由FindTableData函数获得)
    # InfoStep: 产品信息所占列数
    # Priceflag: 一个日期对应三个价格(主流、底端、高端) Priceflag=1; 一个日期对应一个价格 Priceflag=2
    # 将所需数据写入fp对应的txt文件


    # DataStep: 每一行中价格数据所占的列数(包括涨跌、人民币价)
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

            # 找到并写入每一行的产品信息
            tempInfo = Info[(rn * InfoStep):((rn + 1) * InfoStep)]
            fp.write(Region + ":" + ":".join(tempInfo) + "\n\n")

            # 写入表头
            fp.write("日期\t\t主流价\t低端价\t高端价\t涨跌差\t涨跌率\n\n")
            i = 0
            while (i < 5):
                # 写入价格
                fp.write(Header[HeaderStart + i] + "\t\t" + Data[rn * DataStep + i * 3] + "\t" \
                         + Data[rn * DataStep + i * 3 + 1] + "\t" + Data[rn * DataStep + i * 3 + 2] + "\t")
                if i == 4:
                    # 写入涨跌
                    fp.write(Data[rn * DataStep + 15] + "\t" + Data[rn * DataStep + 16])
                    if RMB == 2:
                        fp.write("\n\n人民币价:\t" + Data[rn * DataStep + 17])
                fp.write("\t\n\n")
                i += 1

            fp.write("\n" + r"#############################" + "\n\n")

    if Priceflag == 2:
        for rn in Row:

            tempInfo = Info[(rn * InfoStep):((rn + 1) * InfoStep)]
            fp.write(Region + ":" + ":".join(tempInfo) + "\n\n")

            fp.write("日期\t\t价格\t涨跌差\t涨跌率\n\n")
            i = 0
            while (i < 5):
                fp.write(Header[HeaderStart + i] + "\t\t" + Data[rn * DataStep + i] + "\t")
                if i == 4:
                    fp.write(Data[rn * DataStep + 5] + "\t" + Data[rn * DataStep + 6])
                    if RMB == 2:
                        fp.write("\n\n人民币价:\t" + Data[rn * DataStep + 7])
                fp.write("\t\n\n")
                i += 1

            fp.write("\n" + r"#############################" + "\n\n")
