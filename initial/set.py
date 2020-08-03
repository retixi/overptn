import pandas as pd
import os
# base_root_path = 'D:\\RTX\\专项\\PTN流量分析\\2017\\excel自动化系统\\流量挂牌系统\\流量挂牌系统（PTN网络）\\基础数据\\基础挂牌数据-PTN网络.xlsx'
# supervise_dir = 'D:\\RTX\专项\\PTN流量分析\\2017\\excel自动化系统\\流量挂牌系统\\流量挂牌系统（PTN网络）\\RedOrangeBlue'
# excel_df = pd.read_excel(base_root_path)
# origin_df = excel_df[excel_df.columns[1:-3]]
# origin_df['统计时间'] = origin_df['统计时间'].astype('str')
# df_count_by_date = origin_df['统计时间'].value_counts().reset_index().sort_index(by=['index'])
# df_count_by_city = origin_df['地市'].value_counts().reset_index().sort_index(by=['index'])

class SetItem:
    def __init__(self,base_root_path,supervise_dir):
        self.base_root_path = base_root_path
        self.supervise_dir = supervise_dir
        self.excel_df = pd.read_excel(base_root_path)
        self.origin_df = self.excel_df[self.excel_df.columns[1:-3]]
        self.origin_df['统计时间'] = self.origin_df['统计时间'].astype('str')
        self.df_count_by_date = self.origin_df['统计时间'].value_counts().sort_index().reset_index()
        self.df_count_by_city = self.origin_df['地市'].value_counts().sort_index().reset_index()

# set_item1 = SetItem(base_root_path = 'D:\\RTX\\专项\\PTN流量分析\\2017\\excel自动化系统\\流量挂牌系统\\流量挂牌系统（PTN网络）\\基础数据\\基础挂牌数据-PTN网络.xlsx',
#                 supervise_dir = 'D:\\RTX\专项\\PTN流量分析\\2017\\excel自动化系统\\流量挂牌系统\\流量挂牌系统（PTN网络）\\RedOrangeBlue')
set_item2 = SetItem(base_root_path  = os.path.join(os.getcwd(),'basedata',"基础挂牌数据-PTN网络.xlsx"),
                supervise_dir = os.path.join(os.getcwd(),"RedOrangeBlue"))

set_item = set_item2