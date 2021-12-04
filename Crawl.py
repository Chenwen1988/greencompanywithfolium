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

# from user_agent import get_user_agent

book = xlwt.Workbook(encoding='utf-8')  # 0.创建一个工作簿
sheet = book.add_sheet("安居客", cell_overwrite_ok=True)  ## 1.创建空表

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'referer': 'https://shanghai.anjuke.com/',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
}
##请求网站信息

def req():
    response = requests.get('https://sh.fang.anjuke.com/', headers=headers)  ##加请求头,如果需要加随机请求头和代理ip的可以看我的别的博客
    return response


# 解析网站
def crawl():
    res = req()
    names = re.findall('<span class="items-name">(.*?)</span>', res.text, re.S)
    places = re.findall('<span class="list-map" target="_blank">\[&nbsp;(.*?)&nbsp;(.*?)&nbsp;\]&nbsp;(.*?)</span>',
                        res.text, re.S)
    huxing_mianji_prices = re.findall('<a class="address"(.*?)<!-- 户型销控信息开关 -->', res.text, re.S)
    return names, places, huxing_mianji_prices


##具体定位户型等详细信息
def details():
    names, places, huxing_mianji_prices = crawl()
    huxing_list = []
    mianji_list = []
    prices_list = []
    for content in huxing_mianji_prices:  ##对每一块进行操作，方便对后续缺失、非结构化数据进行处理。
        strings = '户型：'
        strings1 = '建筑面积：'

        if strings in content:  # 在小范围内查找
            huxing = re.findall('户型：.*?<span>(.*?) ', content, re.S)[0]
        else:
            huxing = "无户型"
        huxing_list.append(huxing)

        if strings1 in content:  # 在每一块里寻找面积
            mianji = re.findall('建筑面积：(.*?)</span>', content, re.S)[0]
        else:
            mianji = "无面积"
        mianji_list.append(mianji)

        price = re.findall('<p class="price(.*?)</p>', content, re.S)[0]
        prices_list.append(price)
    return names, places, huxing_list, mianji_list, prices_list  # 返回户型,面积,价格


# 清洗数据,因为是用正则表达式提取的，所以要将无关的符号去掉
def select_datas():
    names, places, huxing_list, mianji_list, prices_list = details()
    final_huxing = []
    final_mianji = mianji_list
    final_prices = []
    # print(prices_list)
    for i in range(len(huxing_list)):
        if "span" in huxing_list[i]:
            huxing_list[i] = huxing_list[i].replace('</span>', '、').replace('/<span>', '')
        else:
            pass
        final_huxing.append(huxing_list[i])

        if '-txt">' in prices_list[i]:
            prices_list[i] = prices_list[i].replace('-txt">', '')
        if 'span' in prices_list[i]:
            prices_list[i] = prices_list[i].replace('<span>', ':').replace('</span>', '')
        if '">' in prices_list[i]:
            prices_list[i] = prices_list[i].replace('">', '')
        final_prices.append(prices_list[i])
    return names, places, huxing_list, mianji_list, prices_list


# 写入表格
def write_to_excel():
    names, places, huxing_list, mianji_list, prices_list = select_datas()  ##调用处理之后的数据
    sheet.write(0, 0, '小区名')  ##2. 创建表头
    sheet.write(0, 1, '地址')
    sheet.write(0, 2, '户型')
    sheet.write(0, 3, '面积')
    sheet.write(0, 4, '价格')
    for i in range(len(names)):
        name = names[i]
        place = places[i]
        huxing = huxing_list[i]
        mianji = mianji_list[i]
        price = prices_list[i]
        sheet.write(i + 1, 0, name)  ##3.写入数据
        sheet.write(i + 1, 1, place)
        sheet.write(i + 1, 2, huxing)
        sheet.write(i + 1, 3, mianji)
        sheet.write(i + 1, 4, price)
    book.save('上海安居客房价数据' + '.xls')


def main():
    write_to_excel()


if __name__ == "__main__":
    main()
