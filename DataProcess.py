import datetime
import time
import pandas as pd
import matplotlib.pyplot as plt
import math

df = pd.read_csv('美国疫情TTtest.csv',nrows=3300)       #nrows是csv中数据的行数，按实际填写要读的总行数
# #df['from'] = df['from'].astype('str')
# df['date'] = [x for x in df['date']]
# #print(df.head())
# #df['date'] = "2021年"+df['date']
# df['date']=df['date'].str.replace('年','-')            #将2021年1月1日转换为2021-01-01格式
# df['date']=df['date'].str.replace('月','-')
# df['date'] = [datetime.datetime.strptime(str(date), u"%Y年%m月%d日") for date in df['date']]

#output_df = pd.concat([df,df['date']], axis=1)
#output_df.to_csv('C:\\Users\\15812\\Desktop\\社交信息传播时序预测算法\\菠萝滞销结果清洗.csv',encoding='utf_8_sig', index=False)
#print(output_df.head())
new_df=df.groupby('date').sum()
#new_df['date']=
#print(df.groupby('date').sum())
print(new_df.head())
new_df.to_csv('美国疫情时间序列.csv',encoding='utf_8_sig')
