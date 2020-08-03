#本文件用于将数据文件从指定服务器上下载到本地
import os,shutil
import datetime,time
from module import ftp
def collectData(start_datestr,end_datestr):
    server_ip = '10.217.2.38'
    hw_ftp = ftp.ftp_conn(server_ip,21,'huawei','Xn_Hw&*01')
    data_dir = os.path.join(os.getcwd(),'origin_data')
    save_dir_hour = os.path.join(os.getcwd(),'origin_data_hour')
    try:
        shutil.rmtree(data_dir)
    except:
        pass
    path_list = []
    path_list.extend(hw_ftp.nlst('/home/huawei'))
    path_list.extend(hw_ftp.nlst('/home/fiber'))
    path_list.extend(hw_ftp.nlst('/home/zte/aaa'))

    start_date = datetime.datetime.strptime(start_datestr,'%Y%m%d')
    end_date = datetime.datetime.strptime(end_datestr,'%Y%m%d')
    days_diff = (end_date-start_date).days
    date_list =[]
    filenames = []
    for i in range(days_diff+1):
        current_date = start_date+datetime.timedelta(i)
        current_datestr = current_date.strftime('%Y%m%d')
        date_list.append(current_datestr)
        print(current_datestr)
        save_dir = os.path.join(data_dir,current_datestr)
        os.makedirs(save_dir)
        for each in path_list:
            if each.find(current_datestr) != -1:
                filename = each.split('/')[-1]
                if filename.split('.')[-1][0:3] == 'xls':
                    ftp.downloadfile(hw_ftp,each,save_dir+'\\'+filename)
                    filenames.append(filename)
        if not os.listdir(save_dir):
            os.rmdir(save_dir)
        else:
            print(current_datestr+'日期数据下载完毕')
    print('下载完毕')
    res =[filenames,date_list]
    return res

def compareList(datelist):
    city_list = [['GROUPOPERCHECKDAYHA', 'ANY', 'ZTE'],
                 ['GROUPOPERCHECKDAYHA', 'HEB', 'FH'],
                 ['GROUPOPERCHECKDAYHA', 'JIZ', 'HW'],
                 ['GROUPOPERCHECKDAYHA', 'JY', 'HW'],
                 ['GROUPOPERCHECKDAYHA', 'KAF', 'HW'],
                 ['GROUPOPERCHECKDAYHA', 'LUH', 'HW'],
                 ['GROUPOPERCHECKDAYHA', 'LUY', 'HW'],
                 ['GROUPOPERCHECKDAYHA', 'NAY', 'HW'],
                 ['GROUPOPERCHECKDAYHA', 'PDS', 'HW'],
                 ['GROUPOPERCHECKDAYHA', 'PUY', 'ZTE'],
                 ['GROUPOPERCHECKDAYHA', 'SHQ', 'HW'],
                 ['GROUPOPERCHECKDAYHA', 'SMX', 'HW'],
                 ['GROUPOPERCHECKDAYHA', 'XCH', 'HW'],
                 ['GROUPOPERCHECKDAYHA', 'XIX', 'ZTE'],
                 ['GROUPOPERCHECKDAYHA', 'XIY', 'HW'],
                 ['GROUPOPERCHECKDAYHA', 'ZHK', 'HW'],
                 ['GROUPOPERCHECKDAYHA', 'ZMD', 'FH'],
                 ['GROUPOPERCHECKDAYHA', 'ZZ', 'HW']]
    filenames = []
    for date in datelist:
        for city in city_list:
            city1 = city.copy()
            city1.append(str(date))
            filenames.append('-'.join(city1))
    return filenames

def dataValidation(filelist,comparelist):
    filenamelist = [each.split('.')[0] for each in filelist]
    miss_files = []
    for each in comparelist:
        if each not in filenamelist:
            miss_files.append(each)
    return miss_files

