# -*- coding: utf-8 -*-
"""
Created on 18:38 2021/4/28

@file: Crawl.py
@author: BBD
@email: chenwen@bbdservice.com
"""

import random
import re
import requests
import xlwt
from lxml import etree
import time
import os
import pandas as pd

# from user_agent import get_user_agent

book = xlwt.Workbook(encoding='utf-8')  # 0.创建一个工作簿
sheet = book.add_sheet("安居客", cell_overwrite_ok=True)  ## 1.创建空表

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'referer': 'https://chengdu.anjuke.com/',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
}


##请求网站信息
 # TODO:
 # FIXME:


def req(url):
    # response = requests.get('https://cd.fang.anjuke.com/loupan/all/p3/', headers=headers)  ##加请求头,如果需要加随机请求头和代理ip的可以看我的别的博客
    # url = 'https://chengdu.anjuke.com/community/p6/'
    # url = 'https://cd.fang.anjuke.com/loupan/all/p3/'
    response = requests.get(url, headers=headers)
    return response


# def __response_to_xml(response):
#     '''将response处理为xml格式数据'''
#     xml = etree.HTML(response.text)
#     return xml

# 解析网站
def crawl(res):
    # res = req(url)

    content = re.findall('<div class="li-img" data-v-3cea202b>(.*?)%', res.text, re.S)

    names = re.findall('<div class="nowrap-min li-community-title" data-v-3cea202b>(.*?)</div>', res.text, re.S)
    address = re.findall('address:(.*?),defaultPhoto', res.text, re.S)
    # tag = []
    # second_house_num = []
    # rental_house_num = []
    # prices = []
    # trend_color = []
    # trend_rate = []
    year = []
    for i in range(len(content)):
        if '<span class="year" data-v-3cea202b>' in content[i]:
            year.append(re.findall('<span class="year" data-v-3cea202b>(.*?)</span>', res.text, re.S))
        else:
            year.append('NULL')

    tag = re.findall('<span class="prop-tag" data-v-3cea202b>(.*?)</span>', res.text, re.S)
    second_house_num = re.findall(r'二手房[(](.*?)[)]</a></span>', res.text, re.S)
    rental_house_num = re.findall(r'租房[(](.*?)[)]</a></span> ', res.text, re.S)

    prices = re.findall('<div class="community-price" data-v-3cea202b><strong data-v-3cea202b>(.*?)</strong>', res.text,
                        re.S)
    trend = re.findall(r'<span class="propor-text propor-(.*?)" data-v-3cea202b>(.*?)</span></div></a>', res.text,
                       re.S | re.DOTALL)
    trend_color = []
    trend_rate = []
    for i in range(len(trend)):
        trend_color.append(trend[i][0])
        trend_rate.append(re.findall(r'[0-9.%]+', trend[i][1])[0])

    return names, year, address, tag, second_house_num, rental_house_num, prices, trend_color, trend_rate


def is_exist_next_page(res):
    page_url_content = re.findall(
        '<div class="pagination page-bar" data-v-29d65fc6 data-v-75150792>(.*?) class="next next-active" data-v-29d65fc6>下一页</a></div>',
        res.text, re.S | re.DOTALL)

    next_page_url = re.findall('<a href="(.*?)"', page_url_content[0], re.S | re.DOTALL)[-1]

    if next_page_url:
        return next_page_url

    return False


##具体定位户型等详细信息
def details(res):
    names, year, address, tag, second_house_num, rental_house_num, prices, trend_color, trend_rate = crawl(res)


def main(city, path):
    city = 'chengdu'
    url = 'https://{}.anjuke.com/community/p1/'.format(city)
    page_num = 1
    while True:
        time.sleep(3)
        print('正在爬取{}第{}页的信息'.format(city, page_num))
        res = req(url)

        names, year, address, tag, second_house_num, rental_house_num, prices, trend_color, trend_rate = crawl(res)
        community_info = pd.DataFrame(
            {'names': names, 'year': year, 'address': address, 'second_house_num': second_house_num,
             'rental_house_num': rental_house_num, 'prices': prices, 'trend_color': trend_color,
             'trend_rate': trend_rate})

        community_info.to_csv(path + 'community_info_{}.csv'.format(page_num), index=False, encoding='gbk')
        # 测试了一下，二手房数据最多50页，但是最好还是根据下一页去获取到下一页的数据
        next_page_url = is_exist_next_page(res)
        if not next_page_url:
            raise MyException(10000, "{}二手房--数据爬取完毕...".format(city))

        url = next_page_url
        page_num += 1


if __name__ == "__main__":

    if not os.path.exists('Community_1'):
        os.mkdir('Community_1')

    path = './Community_1/'

    main('cd', path)
