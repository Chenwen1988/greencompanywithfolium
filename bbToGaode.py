# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 23:47:13 2021

@author: Administrator
"""

import math 

def bbToGaode(data):
    """ 百度坐标转高德坐标 :param lon: :param lat: :return: """ 
    lon = data['lng']
    lat = data['lat']
    PI = 3.14159265358979324 * 3000.0 / 180.0 
    x = lon - 0.0065 
    y = lat - 0.006 
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * PI) 
    theta = math.atan2(y,x)-0.000003 * math.cos(x * PI)
    return round(z * math.sin(theta),6)
#round(z * math.cos(theta),6)
#,round(z * math.sin(theta),6)