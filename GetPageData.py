# -*- coding:utf-8 –*-

import urllib
import urllib2


# Get one URL
def GetOneURL(url, isGetMethod, values={}, timeout=3):
    # creat the url and get the page
    user_agent = r"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
    headers = {'User-Agent': user_agent}
    data = urllib.urlencode(values)
    if (isGetMethod):
        geturl = url + "?" + data
        request = urllib2.Request(url=geturl, headers=headers)
    else:
        request = urllib2.Request(url=url, data=data, headers=headers)

    response = urllib2.urlopen(url=request, timeout=timeout)
    page = response.read()
    return page


def GetOneURLWithCookie(url, opener, isGetMethod, values={}, timeout=10):
    # creat the url and get the page
    user_agent = r"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
    headers = {'User-Agent': user_agent}
    data = urllib.urlencode(values)

    if (isGetMethod):
        geturl = url + "?" + data
        request = urllib2.Request(url=geturl, headers=headers)
    else:
        request = urllib2.Request(url=url, data=data, headers=headers)

    response = opener.open(fullurl=request, timeout=timeout)
    page = response.read()
    return page
