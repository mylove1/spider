# -*- coding: utf-8 -*-
import urllib2
import re
from BeautifulSoup import BeautifulSoup

aaa = 3640

'''
藏宝阁url
    http://xyq.cbg.163.com/cgi-bin/query.py?act=query
    &server_id=192&areaid=7&server_name=%C4%B5%B5%A4%CD%A4&page=1&query_order=&kindid=42&kind_depth=4
'''

baseUrl = "http://xyq.cbg.163.com/cgi-bin/query.py?act=query"
temp = "&"
server_id = "192"
areaid = "7"
server_name="%C4%B5%B5%A4%CD%A4"
page="1"
query_order="price+DESC"
kindid="23-2" # 梦幻币 kindid=42&kind_depth=4

url1 = baseUrl + temp +"server_id=" + server_id + temp + "areaid=" + areaid +temp\
        + "server_name=" + server_name + temp + "page=" + page +temp + "query_order=" + query_order\
        + temp + "kindid=42&kind_depth=4"
print(url1)
fp = urllib2.urlopen(url1)

try:
    s = fp.read().decode("gb2312", 'ignore')  # 把gb2312修改成网页的编码
    # print(unicode(s,'gb2312').encode('utf-8'))  #处理读取网页内容中的中文乱码
    s = re.sub("charset=gb2312", "charset=utf-8", s, re.I)
    s = s.encode('utf-8', 'ignore')
except:
    s = fp.read()

soup = BeautifulSoup(s)
polist = soup.findAll('span')
print(polist[0].contents[0])  # 获取第一个span标签中的内容