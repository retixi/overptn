from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import pandas as pd
import numpy as np
from module.data_handle import *
from module.data_collect import *
from module.networkdata_combine import *
from module.link_combine import *
from initial.set import set_item
from module.supervise import *
import os,json,re
root_dir = os.getcwd()
datelist = set_item.origin_df['统计时间'].value_counts().sort_index(ascending=False).index
origindate = datelist[0]

sidebar_status0 = {
    'collect':'nav-item',
    'collect0':'nav-link',
    'table':'nav-item',
    'table0': 'nav-link',
    'table1':'nav-link',
    'table2':'nav-link',
    'dashboard':'nav-item',
    'dashboard0': 'nav-link',
    'dashboard1':'nav-link',
    'dashboard2':'nav-link',
    'favorlink':'nav-item',
    'favorlink0':'nav-link',
    'datamap': 'nav-item',
    'datamap0': 'nav-link',
    'datamap1': 'nav-link',
    'datamap2': 'nav-link',

}
# Create your views here.
def root(request):
    return HttpResponseRedirect('../dataCollect')

def dataCollect(request):
    sidebar_status = sidebar_status0.copy()
    sidebar_status['collect0']='nav-link active'
    context = {
                'downloads': [],
                'sidebarstatus': sidebar_status,
               'missfiles': [],
               'startdate':'请输入8位起始日期',
                'enddate':'请输入8位截止日期',
                'combinestatus': '待合并',
               'datelist':datelist

    }
    return render(request,'dataCollect.html',context)

def dateInput(request):
    # json_result = json.loads(request.body)
    if request.method == "POST":
        startdate = request.POST.get('startdate','')
        enddate = request.POST.get('enddate','')
        res = collectData(startdate,enddate)
        comparelist = compareList(res[1])
        miss_files = dataValidation(res[0],comparelist)
        context = {'downloads':res[0],
                   'sidebarstatus': sidebar_status0,
                   'missfiles':miss_files,
                   'startdate':startdate,
                    'enddate':enddate,
                   'combinestatus': '待合并'

                   }
        return render(request,'dataCollect.html',context)

def ringList(request):
    # ringdate = getDate(request,ringdata.df,origindate)
    ringdf = set_item.origin_df
    context = ringdf.to_dict('split')
    context['currentdate'] = origindate
    context['datelist'] =  datelist
    context['columns'] = set_item.origin_df.columns

    sidebar_status = sidebar_status0.copy()
    sidebar_status['table']='nav-item menu-open'
    sidebar_status['table1']='nav-link active'
    context['sidebarstatus'] = sidebar_status
    context['url'] = '../ringList/'
    # if ringdate[2] == 2:
    #     try:
    #         save_file_path = request.GET.get('pathselect')
    #         ringdf.to_excel(save_file_path,index=False)
    #     except:
    #         filename = '环网列表-'+request.GET.get('dateselect')+'.xlsx'
    #         save_file_path = os.path.join(root_dir, 'excel', filename)
    #         ringdf.to_excel(save_file_path,index=False)
    return render(request, 'ringList.html', context)

def ring_dashboard(request):
    ringdate = getDate(request,set_item.origin_df,origindate)
    ringdf, dateselect, status, send_email = ringdate
    if send_email:
        superviseStart(set_item.base_root_path)
    else:
        print('不发送邮件')
    file_path = os.path.join(root_dir, 'data', 'bts.csv')
    # position_dict = pd.read_csv(file_path).to_dict('split')
    position_dict = {'data':[]}
    ringdata_bydate = SummaryData(ringdf)
    ring_counts = ringdata_bydate.get_count_by_city()
    ringcount_by_last_date = set_item.df_count_by_date[:]
    overcount = ringdata_bydate.overdf['环网名称'].count()

    df_city_count = set_item.origin_df[set_item.origin_df['统计时间']==dateselect]['地市'].value_counts().sort_index().reset_index()
    df_city_count['index'] = df_city_count['index'].astype('str').str.split('市').str[0]

    dict_city_count = df_city_count.to_dict('split')
    list_city_count = [{'name': dict_city_count['data'][i][0], 'value': dict_city_count['data'][i][1]} for i in
                range(len(dict_city_count['data']))]
    sidebar_status = sidebar_status0.copy()
    sidebar_status['dashboard'] = 'nav-item menu-open'
    sidebar_status['dashboard1'] = 'nav-link active'
    context = {
        'sidebarstatus':sidebar_status,
        'currentdate':ringdate[1],
        'datelist':datelist,
        'ringcount':{
            'index':df_city_count['index'],
            'values':df_city_count['地市']},
        'ringcount_by_last_date':{
            'index':ringcount_by_last_date['index'],
            'values':ringcount_by_last_date['统计时间']
        },
        'citycount':list_city_count,

        'overcount': overcount,
        'count':21844,
        'overratio':round(100*overcount/21844,2),
        'peakavg': round(ringdf['带宽利用率忙时均值'].mean()*100,1),
        'data': position_dict['data']
        }

    return render(request, 'ring_dashboard.html', context)

def link_dashboard(request):

    sidebar_status = sidebar_status0.copy()
    sidebar_status['dashboard'] = 'nav-item menu-open'
    sidebar_status['dashboard2'] = 'nav-link active'
    context = {
        'sidebarstatus':sidebar_status,
        }

    return render(request, 'link_dashboard.html', context)

def linkList(request):

    sidebar_status = sidebar_status0.copy()
    sidebar_status['dashboard'] = 'nav-item menu-open'
    sidebar_status['dashboard2'] = 'nav-link active'
    context = {
        'sidebarstatus':sidebar_status,
        }

    return render(request, 'root.html', context)

def dataCombine(request):
    path1 = networkCombine()
    path2 = link_combine()
    context = {'downloads': [],
               'missfiles': [],
               'sidebarstatus': sidebar_status0,
               'startdate': '请输入8位起始日期',
               'enddate': '请输入8位截止日期',
               'combinestatus':'合并的网络文件已输出至：'+path1+'\n'+'合并的网络文件已输出至：'+path2
               }
    global ringdata
    global linkdata
    global datelist
    global origindate
    try:
        ringdata = RingData(pd.read_csv(ring_file_path))
        linkdata = LinkData(pd.read_csv(link_file_path))
        datelist = ringdata.df['dates'].value_counts().sort_index().index
    except:
        ringdata = pd.DataFrame()
        linkdata = pd.DataFrame()
        datelist = ['无可用日期']
    origindate = datelist[0]
    return render(request,'dataCollect.html',context)

def outLink(request):
    sidebar_status = sidebar_status0.copy()
    sidebar_status['favorlink0']='nav-link active'
    context = {'sidebarstatus':sidebar_status,}
    return render(request, 'outLink.html',context)

def userhelp(request):
    context = {'sidebarstatus':sidebar_status0,}
    return render(request, 'userhelp.html',context)

def dataMap(request):
    sidebar_status = sidebar_status0.copy()
    sidebar_status['datamap'] = 'nav-item menu-open'
    sidebar_status['datamap1'] = 'nav-link active'
    ringdate = getDate(request, set_item.origin_df, origindate)
    ringdf = ringdate[0]
    ringdf['地市'] = ringdf['地市'].str.split('市').str[0]
    print(ringdf['地市'])
    ringpeaks = pd.pivot_table(ringdf,'带宽利用率忙时均值','地市',aggfunc="count")
    ringdict = ringpeaks.to_dict('split')
    ringlist = [{'name':ringdict['index'][i],'value':ringdict['data'][i][0]} for i in range(len(ringdict['data']))]
    print(ringlist)
    context = {
        'sidebarstatus': sidebar_status,
        'currentdate': ringdate[1],
        'datelist': datelist,
        'ringpeaks':ringlist,
    }

    return render(request, 'dataMap.html',context)

def dataMapHeat(request):
    file_path = os.path.join(root_dir, 'data', 'bts.csv')
    position_dict = pd.read_csv(file_path).to_dict('split')
    sidebar_status = sidebar_status0.copy()
    sidebar_status['datamap'] = 'nav-item menu-open'
    sidebar_status['datamap2'] = 'nav-link active'
    context = {'sidebarstatus':sidebar_status,
                'data':position_dict['data']
    }
    return render(request,'dataMapHeat.html',context)
