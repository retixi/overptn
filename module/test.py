from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import pandas as pd
from module.data_handle import *
from module.data_collect import *
from module.networkdata_combine import *
from module.link_combine import *
import os,json
root_dir = os.path.dirname(os.getcwd())

ring_file_path = os.path.join(root_dir,'data','network.csv')
link_file_path = os.path.join(root_dir,'data','corelink.csv')
df = pd.DataFrame()
df.sort_index()

print(ring_file_path)
ringdata = RingData(pd.read_csv(ring_file_path))
linkdata = LinkData(pd.read_csv(link_file_path))
datelist = ringdata.df['dates'].value_counts()
print(datelist.sort_index().index)