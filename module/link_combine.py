import pandas as pd
from module.combine import GetDf
import gc
import os

def GetLinkDf(sheet_number,type,temp_filepath=None):
    filelist = os.listdir(os.path.join(os.getcwd(),'origin_data'))
    data_paths = [os.path.join(os.getcwd(),'origin_data',each) for each in os.listdir(os.path.join(os.getcwd(),'origin_data'))]
    df0 = pd.read_excel(os.path.join(os.getcwd(),'data','start.xls'),sheet_number)
    initial_columns = df0.columns
    print(df0)
    for data_path in data_paths:
        file_paths = [os.path.join(data_path,each) for each in os.listdir(data_path)]
        for filepath in file_paths:
            df1 = pd.read_excel(filepath,sheet_number,header=0)
            df1.columns = initial_columns
            df1['日期'] = data_path.split('\\')[-1]
            try:
                if df1['地市'].iloc[1] =='驻马店' or df1['地市'].iloc[1] =='鹤壁':
                    df1['链路日峰值利用率(填百分数)'] = df1['链路日峰值利用率(填百分数)']*100
                    df1['链路日忙时均值利用率(填百分数)'] = df1['链路日忙时均值利用率(填百分数)']*100
                df0 = pd.concat([df0,df1])
                del df1
                gc.collect()
            except:
                pass
    df0['分类'] =type
    df0=df0.fillna(0)
    df0.to_csv(temp_filepath,index=False)
    del df0
    gc.collect()
    print(temp_filepath+'文件生成完毕,内存已回收')

def link_combine():
    df = pd.DataFrame()
    sr = pd.Series()
    corelink_path = os.path.join(os.getcwd(),'data','corelink.csv')
    GetLinkDf(11,'核心链路',corelink_path)
    return corelink_path