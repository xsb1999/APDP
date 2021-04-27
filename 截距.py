
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os
import statsmodels.api as sm
from statsmodels.formula.api import ols


# In[2]:


def readFile(f1, f2):
    df1 = pd.read_csv(f1, encoding='gbk', engine='python')
    df2 = pd.read_csv(f2, encoding='gbk', engine='python')
    df = pd.merge(df1, df2, on = 'Date and hour')
    df.index = range(len(df))
    return df


# In[3]:


def cal_intercept(df,x,y):
    x1 = list(1 / df[x])
    y1 = list(df[y])

    df_cal = pd.DataFrame({'x':x1, 'y':y1})
    model = ols('y ~ x',data=df_cal).fit()
    
    intercept = model.params['Intercept']
    intercept_se = model.bse['Intercept']
    P_value = model.f_pvalue
    R_square = model.rsquared
    
    return intercept,intercept_se,P_value,R_square


# In[4]:


def loop(df,x_name,y_name,m):
    res_intercept = []
    res_intercept_se = []
    res_R_square = []
    res_P_value = []
    res_day = []
    
    flag = False
    
    try:
        left = int(m.split(',')[0])
        right = int(m.split(',')[1])
    except:
        print('请输入正确时间区间格式！')
        return
    
    if left > 23 or left < 0 or right > 23 or right < 0:
        print('请输入正确时间范围！')
        return
    
    # 例如：(21,3，flag为True) (10,20,flag为False)
    flag = left > right
        
    i = 0
    while i < len(df):
        for j in range(i+1, len(df)):
            day_i = df['Date and hour'][i][0:10]
            day_j = df['Date and hour'][j][0:10]

            # 最后一个，跳出while循环
            if j == len(df)-1:
                # 晚上
                if flag:
                    df_tmp = pd.concat([df[i:i+left+1], df[i+right:j+1]])
                    
                else:
                    df_tmp = df[i+left: i+right+1]
                    
                intercept_tmp,intercept_se_tmp,P_value_tmp,R_square_tmp = cal_intercept(df_tmp, x_name, y_name)
                res_intercept.append(intercept_tmp)
                res_intercept_se.append(intercept_se_tmp)
                res_R_square.append(R_square_tmp)
                res_P_value.append(P_value_tmp)
                res_day.append(day_i)
                
                i = len(df)
                break
                
                
            if day_i != day_j:
                # 晚上
                if flag:
                    df_tmp = pd.concat([df[i:i+left+1], df[i+right:j]])
                                       
                else:
                    df_tmp = df[i+left: i+right+1]
                
                intercept_tmp,intercept_se_tmp,P_value_tmp,R_square_tmp = cal_intercept(df_tmp, x_name, y_name)
                res_intercept.append(intercept_tmp)
                res_intercept_se.append(intercept_se_tmp)
                res_R_square.append(R_square_tmp)
                res_P_value.append(P_value_tmp)
                res_day.append(day_i)

                i = j
                break                

    return res_intercept,res_intercept_se,res_P_value,res_R_square,res_day


# In[5]:


def loop1(df_all,x_name,y_name,m):
    df1 = df_all[0]
    df2 = df_all[1]
    df3 = df_all[2]
    df1.rename(columns={x_name[0]:'x',y_name[0]:'y'}, inplace=True)
    df2.rename(columns={x_name[1]:'x',y_name[1]:'y'}, inplace=True)
    df3.rename(columns={x_name[2]:'x',y_name[2]:'y'}, inplace=True)
    res_intercept = []
    res_intercept_se = []
    res_R_square = []
    res_P_value = []
    res_day = []
    flag = False
    
    try:
        left = int(m.split(',')[0])
        right = int(m.split(',')[1])
    except:
        print('请输入正确时间区间格式！')
        return
    
    if left > 23 or left < 0 or right > 23 or right < 0:
        print('请输入正确时间范围！')
        return
    
    # 例如：(21,3，flag为True) (10,20,flag为False)
    flag = left > right
        
    i = 0
    while i < len(df1):
        for j in range(i+1, len(df1)):
            day_i = df1['Date and hour'][i][0:10]
            day_j = df1['Date and hour'][j][0:10]

            # 最后一个，跳出while循环
            if j == len(df1)-1:
                # 晚上
                if flag:
                    df_tmp1 = pd.concat([df1[i:i+left+1], df1[i+right:j+1]])
                    df_tmp2 = pd.concat([df2[i:i+left+1], df2[i+right:j+1]])
                    df_tmp3 = pd.concat([df3[i:i+left+1], df3[i+right:j+1]])
                    df_tmp = pd.concat([df_tmp1,df_tmp2,df_tmp3])
                else:
                    df_tmp1 = df1[i+left: i+right+1]
                    df_tmp2 = df2[i+left: i+right+1]
                    df_tmp3 = df3[i+left: i+right+1]
                    df_tmp = pd.concat([df_tmp1,df_tmp2,df_tmp3])
                intercept_tmp,intercept_se_tmp,P_value_tmp,R_square_tmp = cal_intercept(df_tmp, 'x', 'y')
                res_intercept.append(intercept_tmp)
                res_intercept_se.append(intercept_se_tmp)
                res_R_square.append(R_square_tmp)
                res_P_value.append(P_value_tmp)
                res_day.append(day_i)
                
                i = len(df1)
                break
                
                
            if day_i != day_j:
                # 晚上
                if flag:
                    df_tmp1 = pd.concat([df1[i:i+left+1], df1[i+right:j]])
                    df_tmp2 = pd.concat([df2[i:i+left+1], df2[i+right:j]])
                    df_tmp3 = pd.concat([df3[i:i+left+1], df3[i+right:j]])
                    df_tmp = pd.concat([df_tmp1,df_tmp2,df_tmp3])                                       
                else:
                    df_tmp1 = df1[i+left: i+right+1]
                    df_tmp2 = df2[i+left: i+right+1]
                    df_tmp3 = df3[i+left: i+right+1]
                    df_tmp = pd.concat([df_tmp1,df_tmp2,df_tmp3])
                intercept_tmp,intercept_se_tmp,P_value_tmp,R_square_tmp = cal_intercept(df_tmp, 'x', 'y')
                res_intercept.append(intercept_tmp)
                res_intercept_se.append(intercept_se_tmp)
                res_R_square.append(R_square_tmp)
                res_P_value.append(P_value_tmp)
                res_day.append(day_i)

                i = j
                break                

    return res_intercept,res_intercept_se,res_P_value,res_R_square,res_day  


# In[6]:


def Run():
    while True:
        os.chdir('E:\\大塔数据处理\\Result\\Hour_Avg')
        
        x = ''
        y = ''
        z = []
        t = []
        
        s = input('请输入S或S1或S2或S3：')
        if s == 'exit':
            print('Bye!')
            break
        if s != 'S' and s != 'S1' and s != 'S2' and s != 'S3':
            print('请输入正确S（S1/S2/S3）')
            break
        
        z.append('S1_[CO2_rec_avg]_ppm_avg_hour.csv')
        z.append('S2_[CO2_rec_avg]_ppm_avg_hour.csv')
        z.append('S3_[CO2_rec_avg]_ppm_avg_hour.csv')
        
        c = input('C13 或 O18：')
        if c == 'exit':
            print('Bye!')
            break
        elif c == 'C13':
            # 文件名
            x = s + '_[CO2_rec_avg]_ppm_avg_hour.csv'
            y = s + '_δ13C‰_avg_avg_hour.csv'
            t.append('S1_δ13C‰_avg_avg_hour.csv')
            t.append('S2_δ13C‰_avg_avg_hour.csv')
            t.append('S3_δ13C‰_avg_avg_hour.csv')
        elif c == 'O18':
            # 文件名
            x = s + '_[CO2_rec_avg]_ppm_avg_hour.csv'
            y = s + '_δ18O‰_avg_avg_hour.csv'
            t.append('S1_δ18O‰_avg_avg_hour.csv')
            t.append('S2_δ18O‰_avg_avg_hour.csv')
            t.append('S3_δ18O‰_avg_avg_hour.csv')
            
        else:
            print('请输入C13或O18！')
            break
        m = input('请输入时间范围(例如：21,3或15,20...)：')
        if m == 'exit':
            print('Bye!')
            break
        
        if s == 'S':
            df_all = []
            df_all.append(readFile(z[0],t[0]))
            df_all.append(readFile(z[1],t[1]))
            df_all.append(readFile(z[2],t[2]))
            x_all = [z[0][0:len(z[0])-4],z[1][0:len(z[1])-4],z[2][0:len(z[2])-4]]
            y_all = [t[0][0:len(t[0])-4],t[1][0:len(t[1])-4],t[2][0:len(t[2])-4]]
            res_intercept,res_intercept_se,res_P_value,res_R_square,res_day = loop1(df_all,x_all,y_all,m)
        else:
            df = readFile(x, y)
            x_ = x[0:len(x)-4]
            y_ = y[0:len(y)-4]
            res_intercept,res_intercept_se,res_P_value,res_R_square,res_day = loop(df,x_,y_,m)
        
        out_res = pd.DataFrame({'Date':res_day, 'Intercept':res_intercept, 'Intercept_SE':res_intercept_se, 'R_Square':res_R_square, 'P_Value':res_P_value})
        # 写入csv文件
        os.chdir('E:\\大塔数据处理\\Result\\Intercept')
        path = ''
        left = m.split(',')[0]
        right = m.split(',')[1]
        if c=='C13':
            path = s+'\\'+s+'_CO2_δ13C_Intercept'+'('+left+'-'+right+')'+'.csv'
        elif c=='O18':
            path = s+'\\'+s+'_CO2_δ18O_Intercept'+'('+left+'-'+right+')'+'.csv'
        else:
            print('请输入C13或O18！')
            break
        out_res.to_csv(path, index = None, encoding = 'gbk')
        print('Done!')
        print('---------------------------')


# In[7]:


Run()

