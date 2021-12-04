# -*- coding: utf-8 -*-
"""
Created on 17:03 2021/4/29

@file: GetHTML.py
@author: BBD
@email: chenwen@bbdservice.com
"""

import urllib.request


def getHtml(url):
    html = urllib.request.urlopen(url).read()
    return html


def saveHtml(file_name, file_content):
    # 注意windows文件命名的禁用符，比如 /
    with open(file_name.replace('/', '_') + ".html", "wb") as f:
        # 写文件用bytes而不是str，所以要转码
        f.write(file_content)


if __name__ == '__main__':
    aurl = "https://chegndu.anjuke.com/community/p1/"
    html = getHtml(aurl)
    saveHtml("community_HTMLStructure", html)
