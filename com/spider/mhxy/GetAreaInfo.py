#!usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import urllib2
import FileUtils



def getAreaInfo(areaUrl='http://res.xyq.cbg.163.com/js/server_list_data.js'):
    '''打开登陆页面'''
    req = urllib2.Request(areaUrl)  # req表示向服务器发送请求#
    response = urllib2.urlopen(req)  # response表示通过调用urlopen并传入req返回响应response#
    the_page = response.read()  # 用read解析获得的HTML文件#
    content = the_page.decode('gbk')
    areainfo = str(content).split(';')[1].split('=')[1]
    areaJson = json.loads(areainfo)

    fileName = areaUrl.split('/')[len(areaUrl.split('/')) - 1]
    FileUtils.saveToFile('jsfiles/'+fileName,content)
    # #获取js文件名称
    # fileName = areaUrl.split('/')[len(areaUrl.split('/'))-1]
    #
    # #保存文件
    # if not os.path.exists("jsfiles/"):
    #     os.mkdir(r'jsfiles/')
    #     if not os.path.exists("jsfiles/"+fileName):
    #         with open("jsfiles/"+fileName, 'wb') as code:
    #             code.write(content)


def readJs(fileName):
    if not os.path.exists(fileName):
        print '文件不存在'
    else:
        alldata = open(fileName, 'rb').read()


if __name__ == '__main__':
    getAreaInfo()