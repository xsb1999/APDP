
# coding: utf-8

# In[1]:


import pandas as pd
import os


# In[2]:


def Do(df, file_name):
    cols = ['Date','0:00:00','1:00:00','2:00:00','3:00:00','4:00:00','5:00:00','6:00:00','7:00:00','8:00:00','9:00:00','10:00:00','11:00:00','12:00:00','13:00:00','14:00:00','15:00:00','16:00:00','17:00:00','18:00:00','19:00:00','20:00:00','21:00:00','22:00:00','23:00:00']
    df_new = pd.DataFrame(columns=cols)
    df_new

    i = 0
    while i < len(df):
        date = df['Date'][i]
        tmp = list(df[file_name][i:i+24])
        tmp.insert(0,date)
        tmp_df = pd.DataFrame(tmp).T
        tmp_df.columns = df_new.columns
        df_new = pd.concat([df_new,tmp_df])
        i = i + 24
    return df_new


# In[3]:


def Run():
    while True:
        os.chdir('E:\\大塔数据处理\\Result\\Hour_Avg')
        file_name = input('请输入文件名：')
        if file_name == 'exit':
            print('Bye!')
            break
        df = pd.read_csv(file_name,encoding='gbk', engine='python')
        file_name = file_name[0:len(file_name)-4]
        df_new = Do(df, file_name)
        os.chdir('E:\\大塔数据处理\\Result\\Hour_Avg\\改变格式')
        path = file_name + '.csv'
        df_new.to_csv(path, index = None, encoding = 'gbk')
        print('Done!')


# In[4]:


Run()

