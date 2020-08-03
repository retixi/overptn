from django.test import TestCase
import pandas as pd

import os,gc
import math
import numpy as np
import pandas as pd
class RingData:
    def __init__(self,df):
        df0 = pd.DataFrame()
        df0['cities'] = df['地市'].str.strip('市')
        df0['nettypes'] = df['分类']
        df0['bandwidthes'] = df['带宽']
        df0['names'] = df['环名称']
        df0['peaks'] = df['日峰值利用率']*100
        df0['busy_avgs'] = df['日忙时均值利用率']*100
        df0['dates'] = df['日期']
        df0 = df0.round({'peaks':1,'busy_avgs':1})
        self.overdf = df0[df0['peaks']>=70]
        self.df = df0
        self.dict = df0.to_dict('split')
        del df
        gc.collect()

class LinkData:
    def __init__(self,df):
        df0 = pd.DataFrame()
        df0['cities'] = df['地市'].str.strip('市')
        df0['bandwidthes'] = df['链路带宽(10GE/40GE)']
        df0['names'] = df['PTN核心链路名称']
        df0['peaks'] = df['链路日峰值利用率(填百分数)'].str.strip('%').astype('float')
        df0['busy_avgs'] = df['链路日忙时均值利用率(填百分数)'].str.strip('%').astype('float')
        df0['dates'] = df['日期']
        df0 = df0.round({'peaks':1,'busy_avgs':1})
        self.df = df0
        self.dict = df0.to_dict('split')
        self.overdf = df0[df0['peaks']>=70]
        del df
        gc.collect()

class SummaryData:
    def __init__(self, df):
        self.df = df
        self.overdf = df[df['带宽利用率忙时均值']>=0.7]
    def get_count_by_city(self):
        count_sr = self.df.groupby('地市').count()['环网名称'].sort_values(ascending=False)
        return count_sr


    def get_overcount_by_city(self):
        count_sr = self.overdf.groupby('地市').count()['环网名称'].sort_values(ascending=False)
        return count_sr


    def get_peakavg_by_city(self):
        peak_sr = self.df.groupby('地市').mean()['带宽利用率忙时均值'].sort_values(ascending=False)
        return peak_sr


    def get_count_by_date(self):
        count_sr = self.df.groupby('dates').count()['环网名称'].sort_values(ascending=False)
        return count_sr

def getDate(request,df,origindate):
        if request.method == "POST":
            try:
                dateselect = request.POST.get('dateselect')
                df = df[df['统计时间']==dateselect]
            except:
                dateselect = 'all'
            status =0
            try:
                send_email = request.POST.get('sendemail')
                if send_email == 1:
                    print('email_send')
            except:
                dateselect = 'all'
            status =0

        else:
            if request.GET.get('dateselect')!=None:
                try:
                    dateselect = int(request.GET.get('dateselect'))
                    df = df[df['统计时间'] == dateselect]
                except:
                    dateselect = origindate
                    pass
                status = 2
            else:
                df = df[df['统计时间'] == origindate]
                dateselect = origindate
                status = 1
            if request.GET.get('sendemail')!=None:
                send_email = True
            else:
                send_email = False
        return df,dateselect,status,send_email

def normfun(x,mu, sigma):
    pdf = np.exp(-((x - mu)**2) / (2* sigma**2)) / (sigma * np.sqrt(2*np.pi))
    return pdf

class Norm:
    def __init__(self,pdseri,xmin,xmax,count):
        self.interval = (xmax-xmin)/count
        self.min = xmin
        self.max = xmax
        self.sigma = np.std(pdseri,ddof = 0)
        self.mu = np.average(pdseri)
        self.x = np.arange(xmin,xmax,self.interval)
        self.y = normfun(self.x,self.mu,self.sigma)
        self.s = np.sum(self.y)
    def getRatio(self,over):
        xrange = np.arange(over, self.max, self.interval)
        yrange = normfun(xrange, self.mu, self.sigma)
        s1 = np.sum(yrange)
        p = s1 / self.s
        return p
    def getDayCount(self,over,threhold):
        p = self.getRatio(over)
        n = int(math.log(1-threhold,1-p))
        return n
    def slice(self):
        s1 = 0
        xlist = self.x.tolist()
        ylist = self.y.tolist()
        while s1/self.s < 0.005:
            s1 = s1 + self.interval*ylist.pop()
            over = xlist.pop()
        return over

def timeoverratio(notoverratio,controlcount,daycount):
    oneday_over_ratio = 1-notoverratio**controlcount
    allday_over_ratio = 1-(1-oneday_over_ratio)**daycount
    return allday_over_ratio