
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os
import glob


# In[2]:


def preparation(file_name):
    df = pd.read_csv(file_name,index_col=False,encoding="gbk")
    df.rename(columns={' δ18O‰_avg':'δ18O‰_avg',' δ18O_Stdev':'δ18O_Stdev'},inplace=True)
    # 获取当前文件的日期
    date = df['Date and time'][0][0:10]
    # 将S1,S2,S3分开
    df_S1 = df[df['Sample_name']=='S1']
    df_S2 = df[df['Sample_name']=='S2']
    df_S3 = df[df['Sample_name']=='S3']
    new_df = pd.concat([df_S1,df_S2,df_S3],axis=0)
    new_df.index = range(len(new_df))
    # 分别获取S1,S2,S3
    df1 = new_df[new_df['Sample_name']=='S1']
    df2 = new_df[new_df['Sample_name']=='S2']
    df3 = new_df[new_df['Sample_name']=='S3']
    df1.index = range(len(df1))
    df2.index = range(len(df2))
    df3.index = range(len(df3))
    return date, df1, df2, df3


# In[3]:


# 将时间转化为小时
def turnDateToHours(df):
    for i in range(len(df)):
        df['Date and time'][i] = df['Date and time'][i][11:13]


# In[4]:


# 计算每小时任意item的平均值和标准差
def cal_avg_of_hours(item, df):
    res = []
    res_std = []
    for j in range(24):
        if j < 10:
            j = '0' + str(j)
        else:
            j = str(j)
        avg = df[item][df['Date and time']==j].mean()
        avg1 = df[item][df['Date and time']==j].std()
        res.append(avg)
        res_std.append(avg1)
    return res, res_std


# In[5]:


# 计算每天任意item的平均值和标准差
def cal_avg_of_days(item, df):
    res = 0
    res_std = 0
    res = df[item].mean()
    res_std = df[item].std()
    return res, res_std


# In[6]:


# 补上具体日期，导出每小时的csv（日期不拆开）
def toCSV_hour(df,out_res_data,date,item_name, num, std):
    
    year = date[6:len(date)]
    month = date[0:2]
    day = date[3:5]

    # 日期格式：2018-05-01 08:00
    out_res_date = year + '-' + month + '-' + day + ' ' + df['Date and time'] + ':' + '00'   
    out_res_date = out_res_date[~out_res_date.duplicated()]
    out_res_date.index = range(len(out_res_date))
    out_res_date = list(out_res_date)
    
    out_res_hour = df['Date and time'] + ':' + '00'
    out_res_hour = out_res_hour[~out_res_hour.duplicated()]
    out_res_hour = list(out_res_hour)
    
    out_res_date1 = [year + '-' + month + '-' + day] * len(out_res_hour)
    out_res = pd.DataFrame({'Date and hour':out_res_date, 'Date':out_res_date1, 'Hour':out_res_hour, item_name:out_res_data, 'STD':std}, columns=['Date and hour', 'Date', 'Hour', item_name, 'STD'])
    # 定义文件名（item_name.csv）
    path = item_name + '.csv'
    if num == 1:
        out_res.to_csv(path, index = None, encoding = 'gbk')
    else:
        out_res.to_csv(path, mode='a', index = None, header=False, encoding = 'gbk')


# In[7]:


# 补上具体日期，导出每天的csv
def toCSV_day(df,out_res_data,date,item_name, num, std):
    # 日期格式：2018-05-01
    year = date[6:len(date)]
    month = date[0:2]
    day = date[3:5]
    out_res_date = [year + '-' + month + '-' + day]
    out_res_std = [std]
    out_res = pd.DataFrame({'Date and hour':out_res_date, item_name:out_res_data, 'STD':out_res_std}, columns=['Date and hour', item_name, 'STD'])
    # 定义文件名（item_name.csv）
    path = item_name + '.csv'
    if num == 1:
        out_res.to_csv(path, index = None, encoding = 'gbk')
    else:
        out_res.to_csv(path, mode='a', index = None, header=False, encoding = 'gbk')


# In[8]:


def Run(original, result, item, item_name, S, type_):
    os.chdir(original)
    all_files = glob.glob('*.txt')
    num = 0
    for file in all_files:
        os.chdir(original)
        date, df1, df2, df3 = preparation(file)
        df_last = None
        if S == 'S1':
            df_last = df1
        elif S == 'S2':
            df_last = df2
        elif S == 'S3':
            df_last = df3
        else:
            print('请输入正确类别：S1/S2/S3')
            return
        # 每小时均值
        if type_ == 'hour':
            turnDateToHours(df_last)
            out_res_data,std = cal_avg_of_hours(item, df_last)
            # 写入csv
            os.chdir(result+'\\Hour_Avg')
            num += 1
            toCSV_hour(df_last, out_res_data, date, S+'_'+item_name+'_hour', num, std)
            print(str(num) + ' / ' + str(len(all_files)))            
        # 每天均值
        elif type_ == 'day':
            out_res_data,std = cal_avg_of_days(item, df_last)
            # 写入csv
            os.chdir(result+'\\Day_Avg')
            num += 1
            toCSV_day(df_last, out_res_data, date, S+'_'+item_name+'_day', num, std)
            print(str(num) + ' / ' + str(len(all_files)))
        else:
            print('请输入正确类别：hour/day')
            return
    print('Done!')


# In[9]:


while True:
    original = 'E:\\大塔数据处理\\Original'
    result = 'E:\\大塔数据处理\\Result'
    item = input('请输入项目名称：')
    if item == 'exit':
        print('Bye!')
        break
    item_name = item + '_avg'
    S = input('请输入S1或S2或S3：')
    if S == 'exit':
        print('Bye!')
        break
    if S != 'S1' and S != 'S2' and S != 'S3':
        print('请输入正确S（S1/S2/S3）')
        break
    type_ = input('请输入hour 或 day：')
    if type_ == 'exit':
        print('Bye!')
        break
    if type_!='hour' and type_!='day':
        print('请输入正确时间选择（hour或day）')
        break
    
    Run(original, result, item, item_name, S, type_)

