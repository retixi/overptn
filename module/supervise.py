import pandas as pd
import numpy as np
import os,datetime,smtplib,shutil
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import make_header
from initial.set import set_item
root_dir = set_item.supervise_dir
filepath = set_item.base_root_path
log_file_path = os.path.join(root_dir,'派单日志','督办记录.xlsx')
color_dict = {'red':'红色',
              'orange': '橙色',
              'blue': '蓝色',
                  }

def getDateDuration(days_delta):
    end = datetime.datetime.now() - datetime.timedelta(1)
    # end = datetime.datetime.now()
    start = end - datetime.timedelta(days_delta)
    start_date = datetime.date(start.year,start.month,start.day).__str__()
    end_date = datetime.date(end.year,end.month,end.day).__str__()
    return [start_date,end_date]

def colorfiler(color,origin_df):
    df = origin_df.set_index('统计时间')
    if color == 'red':
        days_duration = 14
    elif color == 'orange':
        days_duration = 7
    else:
        days_duration = 0
    start_date,end_date = getDateDuration(days_duration)
    df = df[start_date:end_date]
    df_pivot = pd.pivot_table(df, index=["环网名称",'地市'],values=['key'],aggfunc=np.count_nonzero)
    df_pivot = df_pivot[df_pivot['key'] > days_duration]
    df_pivot = df_pivot.reset_index()
    df_pivot.columns = ['环网名称','地市','越限天数']
    df_pivot['越限天数'] = df_pivot['越限天数'] + 6
    return df_pivot

def citySplit(df,colorset,leaderset):
    cities = df['地市'].drop_duplicates().tolist()

    df_city_allcolor = []
    for city in cities:
        filename = color_dict[colorset] + "预警-" + leaderset + '-' + city + ".xlsx"
        file_path = os.path.join(root_dir,'文件列表',filename)
        df_city = df[df['地市'] == city]
        df_city['督办时间'] = datetime.date.today()
        write_to_excel(df_city,file_path,False)
        df_city_allcolor.append(df_city)
    return df_city_allcolor


def manage_df(file_path):
    df_all = []
    df = pd.read_excel(file_path)
    colors = ['blue','orange','red']
    leaders = ['部门副经理','部门经理','公司经理']
    for i in range(len(colors)):
        for j in range(i+1):
            leader_df = pd.read_excel(os.path.join(root_dir,"督办列表",colors[j]+".xlsx"))
            try:
                df_color = pd.merge(colorfiler(colors[i], df), leader_df)
                df_color['预警级别'] = colors[i]
                df_all.extend(citySplit(df_color,colors[i],leaders[j]))
            except:
                pass
    return df_all

def write_to_excel(df,file_path,isadd):
    if isadd:
        writer = pd.ExcelWriter(file_path, engine='openpyxl')
        df.to_excel(excel_writer=writer, index=None)
        writer.save()
        writer.close()
    else:
        df.to_excel(file_path, index=False)

def send_enclosure(from_addr="rentingxi@ha.chinamobile.com",
                   pwd="Rtx55555",
                   to_addr="rentingxi@ha.chinamobile.com",
                   city="测试",
                   color="蓝色",
                   attatchment_path="d:\\vba.txt"
                   ):
    # 1.发件人、授权码，收件人信息


    # 2.创建实例对象，设置主题等信息
    msg = MIMEMultipart()
    msg["Subject"] = city+color+"PTN网络流量越限预警"
    msg["From"] = from_addr
    msg["To"] = to_addr

    # 邮件内容（按每个部分）
    part1 = part1 = MIMEText(city+'分公司出现'+color+"PTN网络流量越限预警，请及时安排人员处理，详情见附件")
    msg.attach(part1)

    # 添加excel附件
    part2 = MIMEText(open(attatchment_path, 'rb').read(),'base64','utf-8')
    filename = attatchment_path.split('\\')[-1]
    part2.add_header('Content-Disposition', 'attachment', filename=filename)
    part2["Content-Type"] = 'application/octet-stream;name="%s"' % make_header([(filename, 'UTF-8')]).encode('UTF-8')
    part2["Content-Disposition"] = 'attachment;filename= "%s"' % make_header([(filename, 'UTF-8')]).encode('UTF-8')
    msg.attach(part2)

    # 3.连接smtp服务器，登录服务器并发送文本
    smtp_server = "smtp.ha.chinamobile.com"
    server = smtplib.SMTP(smtp_server, 25)
    server.login(from_addr, pwd)
    server.sendmail(from_addr, to_addr, msg.as_string())  # as_string（）把MIMEText变成一个str
    print(filename+'已发送至：' + to_addr)
    server.close()

def setDir(filedir):
    if not os.path.exists(filedir):
        os.mkdir(filedir)
    else:
        shutil.rmtree(filedir)
        os.mkdir(filedir)

def superviseStart(filepath):
    file_dir = os.path.join(root_dir,'文件列表')
    setDir(file_dir)
    df_list = manage_df(filepath)
    if len(df_list) == 0:
        print('本次无督办')
    else:
        for filename in os.listdir(file_dir):
            filepath = os.path.join(root_dir,'文件列表',filename)
            df = pd.read_excel(filepath,index=None)
            mail_list = df['邮箱'].drop_duplicates().tolist()
            city = df['地市'].drop_duplicates().tolist()[0]
            color = df['预警级别'].drop_duplicates().tolist()[0]
            for each in mail_list:
                send_enclosure(to_addr=each,city=city,color=color_dict[color],attatchment_path=filepath)
        df_log = pd.read_excel(log_file_path)
        df_list.append(df_log)
        df_log = pd.concat(df_list)
        df_log.to_excel(log_file_path,index=False)
        print('本次督办结束')
