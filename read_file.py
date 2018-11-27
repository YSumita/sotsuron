
# coding: utf-8

# # **バイナリファイルからあれこれするための関数達**

# ### **必要な関数・ライブラリ**

# In[1]:

import numpy as np


# In[115]:

def process_ic0(x):
    '''
    ic0データの-8888, -9999に対応するための関数
    read_ic0内で使う
    '''
    if x < 0:
        return -1
    return x


# In[116]:

def read_ic0(path):
    '''
    指定されたpathのic0を読んで返す
    '''
    data = np.fromfile(path, np.int16, -1)
    vfunc = np.vectorize(lambda x : process_ic0(x))
    data = vfunc(data)
    data = data.reshape(900, 900)
    # count_sum.f95とデータの読み込み方向が違うので転置
    data = data.T
    return data


# In[148]:

def read_sum_dat_by_(by="year", path = "data/sum.dat"):
    '''
    sum.datを読むためのプログラム
    '''

    # 13年間のデータを地点毎に格納
    # 今までのデータを用いて予測するときに使える
    if by == "place":
        sum_ices = np.zeros((90, 70, 13))
        no_ice_days = np.zeros((90, 70, 13))

        for line in open(path, "r"):
            sum_ic = float(line[1:9])
            no_ice_day = float(line[12:18])
            i = int(line[19:22])
            j = int(line[22:25])
            year = int(line[25:27])

            sum_ices[i-1][j-1][year-1] = sum_ic
            no_ice_days[i-1][j-1][year-1] = no_ice_day

    # 地点毎のデータを年ごとに格納
    # 可視化するときに使える
    elif by == "year":
        sum_ices = np.zeros((13, 90, 70))
        no_ice_days = np.zeros((13, 90, 70))

        for line in open(path, "r"):
            sum_ic = float(line[1:9])
            no_ice_day = float(line[12:18])
            i = int(line[19:22])
            j = int(line[22:25])
            year = int(line[25:27])

            sum_ices[year-1][i-1][j-1] = sum_ic
            no_ice_days[year-1][i-1][j-1] = no_ice_day

    else:
        print("-- unknown sort keyword --")
        sum_ices = np.nan
        no_ice_days = np.nan

    return sum_ices, no_ice_days


# In[151]:

def read_resampled_IC0_by_(path, by="year"):
    '''
    90 * 70にリサンプリングしたIC0データを読む
    '''

    # 13年間のデータを地点毎に格納
    # 今までのデータを用いて予測するときに使える
    if by == "place":
        sum_ices = np.zeros((90, 70, 13))

        for line in open(path, "r"):
            sum_ic = float(line[0:9])
            i = int(line[9:12])
            j = int(line[12:15])
            year = int(line[15:18])

            sum_ices[i-1][j-1][year-1] = sum_ic

    # 地点毎のデータを年ごとに格納
    # 可視化するときに使える
    elif by == "year":
        sum_ices = np.zeros((13, 90, 70))

        for line in open(path, "r"):
            sum_ic = float(line[0:9])
            i = int(line[9:12])
            j = int(line[12:15])
            year = int(line[15:18])

            sum_ices[year-1][i-1][j-1] = sum_ic

    else:
        print("-- unknown sort keyword --")
        sum_ices = np.nan
        no_ice_days = np.nan

    return sum_ices

def read_daily_IC0_by_(path, by="place", duration=134):
    '''
    90 * 70にリサンプリングしたIC0データを読む
    '''

    # 13年間のデータを地点毎に格納
    # 今までのデータを用いて予測するときに使える
    if by == "place":
        daily_ice = np.zeros((90, 70, duration))

        for line in open(path, "r"):
            ic = float(line[0:9])
            i = int(line[9:13])
            j = int(line[13:17])
            hdk = int(line[17:21])

            daily_ice[i-1][j-1][hdk-1] = ic

    # 地点毎のデータを年ごとに格納
    # 可視化するときに使える
    elif by == "day":
        daily_ice = np.zeros((duration, 90, 70))

        for line in open(path, "r"):
            ic = float(line[0:9])
            i = int(line[9:13])
            j = int(line[13:17])
            hdk = int(line[17:21])

            daily_ice[hdk-1][i-1][j-1] = ic

    else:
        print("-- unknown sort keyword --")
        daily_ice = np.nan

    return daily_ice
