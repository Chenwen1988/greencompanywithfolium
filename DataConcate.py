# -*- coding: utf-8 -*-
"""
Created on 17:48 2021/4/30

@file: DataConcate.py
@author: BBD
@email: chenwen@bbdservice.com
"""

import pandas as pd
import numpy as np
import os

file = os.listdir('./Bank_1')

BANK = pd.DataFrame()
for f in file:
    # if 'BANK_Loc' in f:
    print(f)
    f_bank = pd.read_csv('./Bank_1/{}'.format(f), encoding='gbk')
    BANK = pd.concat([BANK, f_bank])

BANK.to_csv('./Bank_info.csv', index=False, encoding='gbk')
