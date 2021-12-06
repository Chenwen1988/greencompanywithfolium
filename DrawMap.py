# -*- coding: utf-8 -*-
"""
Created on 14:08 2021/4/22

@file: GDAPI.py
@author: BBD
@email: chenwen@bbdservice.com
"""

import folium
import pandas as pd
import numpy as np
import os

from folium.plugins import HeatMap

# ['ABC_BANK_info.csv',
#  'BOCOM_BANK_info.csv',
#  'BOC_BANK_info.csv',
#  'CCB_BANK_info.csv',
#  'CDRC_BANK_info.csv',
#  'CEB_BANK_info.csv',
#  'CIB_BANK_info.csv',
#  'CITIC_BANK_info.csv',
#  'CMB_BANK_info.csv',
#  'ICBC_BANK_info.csv',
#  'PINGAN_BANK_info.csv',
#  'PSBC_BANK_info.csv',
#  'SCTF_BANK_info.csv']
def lat_lng(bankname):
    data = pd.read_csv(os.path.join(_path,f"Bank_1/{bankname}.csv"), encoding='gbk')
    
    data['lat'] = data.location.apply(lambda x:x.split(',')[1])
    data['lng'] = data.location.apply(lambda x:x.split(',')[0])
    
    return data

# array(['新都区', '郫都区', '金牛区', '蒲江县', '青白江区', '青羊区', '双流区', '成华区', '锦江区',
#        '武侯区', '龙泉驿区', '简阳市', '金堂县', '新津区', '邛崃市', '彭州市', '崇州市', '温江区',
#        '都江堰市', '大邑县'], dtype=object)
def area_select(data,area):
    
    return data.loc[data.adname == area,['address', 'adname', 'cityname', 'name','pname', 'tel','lat', 'lng']]

def draw_dot(data):
    locations = data[['Gaode_lat','Gaode_lon']]
    locations = locations.dropna(how = 'any')

    san_map = folium.Map(location=[29.552596,106.572744], 
                         zoom_start=12, 
                         tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
                         attr='default',
                         width='100%', 
                         height='100%')

    incidents = folium.map.FeatureGroup()
    for lat, lng, in zip(locations.Gaode_lat, locations.Gaode_lon):
        incidents.add_child(
            folium.CircleMarker(
                [lat, lng],
                radius=1, # define how big you want the circle markers to be
                color='red', # define the circle color
                fill=True,
                fill_color='red',
                fill_opacity=0.4
            )
        )

    san_map.add_child(incidents)
    
    heatdata = locations[['Gaode_lat','Gaode_lon']].values.tolist()
    HeatMap(heatdata).add_to(san_map)
    
    return san_map

def draw_heat(data):
    locations = data[['lat','lng']]
    locations = locations.dropna(how = 'any')

    # 选择的map中心坐标为天府广场经纬度
    san_map = folium.Map(location=[30.657154,104.065971], zoom_start=12, width='100%', height='100%')

    # Convert data format
    heatdata = locations[['lat','lng']].values.tolist()

    # add incidents to map
    HeatMap(heatdata).add_to(san_map)
    
    return san_map

if __name__ == '__main__':
    

    _path = os.getcwd()
    
    # 读取银行经纬度数据
    # TODO：银行类型可以做区分：ATM\24小时营业网点\支行等
#    ICBC_BANK = lat_lng('ICBC_BANK_info')
#    ABC_BANK = lat_lng('ABC_BANK_info')
#    
#    ICBC_BANK_wuhou = area_select(ICBC_BANK,'武侯区')
#    
#    ICBC_BANK_heat_map = draw_heat(ICBC_BANK)
#    ICBC_BANK_heat_map.save('./ICBC_BANK_heat_map_chengdu.html')
    if not os.path.exists('./DotMapGaode'):
        os.mkdir('./DotMapGaode')
    
#    GreenCompanyInfo = pd.read_csv('./GreenCompanyInfo_1.csv',dtype = {'company_gis_lon':np.float,'company_gis_lat':np.float})
#    
#    GreenCompanyInfo.rename(columns = {'company_gis_lat':'Gaode_lat','company_gis_lon':'Gaode_lon'},inplace = True)
#    regorrg = ['重庆市南岸区市场监督管理局', '重庆市江北区市场监督管理局', '重庆市北碚区市场监督管理局',
#       '重庆市沙坪坝区市场监督管理局', '重庆市渝北区市场监督管理局', '重庆市江津区市场监督管理局',
#       '重庆高新技术产业开发区管理委员会市场监督管理局', '重庆市巴南区市场监督管理局', '重庆市渝中区市场监督管理局',
#       '重庆市万州区市场监督管理局']
#    
#    for area in regorrg:
#        _location = GreenCompanyInfo[(GreenCompanyInfo.Gaode_lat != 0) & (GreenCompanyInfo.regorg == area)]
#        dot_map = draw_dot(_location)
#        dot_map.save(f'./DotMapBaidu/{area}.html')
        
    CHONGQINGCOM_location = pd.read_csv('./location/CHONGQINGCOM_location.csv',sep = ',')
    for area in CHONGQINGCOM_location['regorg'].unique():
        _location = CHONGQINGCOM_location[(CHONGQINGCOM_location.location != '查询失败') & (CHONGQINGCOM_location.regorg == area)]
        _location['Gaode_lat'] = _location['location'].apply(lambda x:x.split(',')[1])
        _location['Gaode_lon'] = _location['location'].apply(lambda x:x.split(',')[0])
        
        dot_map = draw_dot(_location)
        dot_map.save(f'./DotMapGaode/{area}.html')
    