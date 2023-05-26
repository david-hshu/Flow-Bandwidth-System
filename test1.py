import os

import pandas as pd
from datetime import datetime

nowTime = datetime.now().strftime('%Y_%m_%d')
print(nowTime)

pwd = 'D:\\flaskProject\\history'

file_list_all = os.listdir(pwd)
file_list_all.sort()
list_len = []

# 查看一个文件夹下有多少个文件
for index in file_list_all:
    pwd_index = pwd + '\\' + index
    list_i = os.listdir(pwd_index)

    list_len.append(sum([os.path.isdir(pwd_index + '\\' + list_index) for list_index in list_i]))

print(list_len)
