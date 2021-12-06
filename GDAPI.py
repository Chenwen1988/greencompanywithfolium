# -*- coding: utf-8 -*-
"""
Created on 14:08 2021/4/22

@file: GDAPI.py
@author: BBD
@email: chenwen@bbdservice.com
"""

import pandas as pd
import requests
import os
import json
import math


def read_key():
    """  持久化key,便于读取 """
    key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'key.txt')
    print(key_path)
    with open(key_path, 'r', encoding='utf-8') as f:
        key = f.read()
        print(key)
    return key


def request_url_get(url):
    """ 请求url方法get方法 """
    try:
        r = requests.get(url=url, timeout=30)
        if r.status_code == 200:
            return r.text
        return None
    except RequestException:
        print('请求url返回错误异常')
        return None


def parse_json(content_json):
    """  解析json函数 """
    result_json = json.loads(content_json)
    return result_json


def request_api(url):
    """ 请求高德api 解析json """
    result = request_url_get(url)
    result_json = parse_json(result)
    return result_json


def get_location(address, city, key):
    # 基于名称或地址返回地理位置信息
    loc_url = f'https://restapi.amap.com/v3/geocode/geo?address={address}&city={city}&key={key}&batch=false&output=JSON'
    # print(address)
    try:
        index_result = request_api(loc_url)
        return index_result.get('geocodes')[0]['location']
    except:
        return '查询失败'


def get_key_match(keywords, city, key, offset):
    # 基于关键词的搜索
    index_url = f'https://restapi.amap.com/v3/place/text?keywords={keywords}&city={city}&' \
                f'offset={offset}&page=1&key={key}&extensions=base'
    index_result = request_api(index_url)
    pages = math.ceil(int(index_result['count']) / offset)  # 算出一共需要的总页数

    if not os.path.exists('Result'):
        os.mkdir('./Result')

    for page in range(1, pages + 1):
        url = f'https://restapi.amap.com/v3/place/text?keywords={keywords}&city={city}&' \
              f'offset={offset}&page={page}&key={key}&extensions=base'
        result = request_api(url)

        result_pois_pd = pd.DataFrame(result.get('pois'))

        result_pois_pd.to_csv('./Result/Community_Loc_{}.csv'.format(page), index=False, encoding='gbk')


if __name__ == '__main__':
    """ 运行函数 """
    path = os.getcwd()
    key = read_key()
    CHONGQINGCOM = pd.read_csv('./CHONGQINGCOM',sep = '\t')
    if not os.path.exists('./location'):
        os.mkdir('./location')
        
    for COM,add in zip(CHONGQINGCOM['company_name'],CHONGQINGCOM['address']):
    add = '重庆市江津区几江街道浩阳街1幢'
        geo = get_location(add, 'chongqing', key)
        with open('./location/Gaode.txt','a') as f:
            f.write(COM+'\t'+str(geo)+'\n')

    #geo_pd.to_csv(os.path.join(path,'geo_f.csv'), encoding='gbk', index=False)
