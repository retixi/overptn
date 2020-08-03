#本文件由于将PTN网络流量数据进行合并并做归一化处理，输出合并文件到gendata文件夹,运行本文件前先运行data_collect.py
import pandas as pd
import gc
import re
import os
from module.combine import GetDf
df = pd.DataFrame()
sr = pd.Series()

def InitialDf(df):
    df['带宽']=df['带宽'].replace(['1GE','2GE','other',0,'0','-','其他'],'GE')
    df['带宽']=df['带宽'].replace(re.compile('^\d\dGE$'),'10GE')
    band_seri = df['带宽'].replace({'GE':1000,'10GE':10000,'100GE':100000,re.compile('^((?!GE).)*$'):1000})
    df['日忙时均值利用率']=df['日忙时均值流速']/band_seri
    df['日峰值利用率']=df['日峰值流速']/band_seri
    return df

def ConbineDf(ac_df0,co_df0,path):
    del co_df0['备注']
    del co_df0['下挂接入环个数']
    co_df0['带宽']='10GE'
    all_df = pd.concat([ac_df0,co_df0])
    del ac_df0
    del co_df0
    all_df = InitialDf(all_df)
    gc.collect()
    all_df['地市'] = all_df['地市'].replace(re.compile('市$'),'')
    return all_df

def networkCombine():
    access_filepath = os.path.join(os.getcwd(),'data','ac.csv')
    convergence_filpath = os.path.join(os.getcwd(),'data','co.csv')
    GetDf(9,'接入层',access_filepath)
    GetDf(10,'汇聚层',convergence_filpath)
    access_df = pd.read_csv(access_filepath)
    print('一级准备完毕')
    convergence_df = pd.read_csv(convergence_filpath)
    print('二级准备完毕')
    path = os.path.join(os.getcwd(),'data')
    print('准备合并')
    try:
        all_df = ConbineDf(access_df,convergence_df,path)
    except:
        pass
    csv_path = os.path.join(path, 'network.csv')
    print(all_df.columns)
    all_df.to_csv(csv_path, index=False)
    return csv_path

