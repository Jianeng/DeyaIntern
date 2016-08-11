# -*- coding: utf-8 -*-

from time import *

from LLDPE import *
from Price import *

print unicode('正在获取LLDPE国内市场价数据...', "utf-8")
GetLLDPE()
print unicode('正在获取PP粉市场信息...', "utf-8")
GetPP()

sleep(3)

region = ("中国地区")
for word in region:
    print word
