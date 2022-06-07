import pandas as pd
import re
from translate import Translator
import csv
import requests
def Chinese(text):      #处理函数
    cleaned = re.findall(r'[\u4e00-\u9fa5]+', text)  #返回列表,用正则表达式筛选出中文
    cleaned = ''.join(cleaned)                      #拼接成字符串
    return cleaned
# def English(text):
#     cleaned = re.findall(r'[a-zA-Z]+', text)  # 返回列表,用正则表达式筛选出英文
#     cleaned = ''.join(cleaned)  # 拼接成字符串
#     return cleaned
def Translation(text):          #翻译，用的是有道翻译的接口，数据传输格式是json
    data = {
        'doctype': 'json',
        'type': 'EN2ZH_CN',             #指定翻译为英译中
        'i': text
    }
    url = "http://fanyi.youdao.com/translate"
    r = requests.get(url, params=data)
    result = r.json()
    changed = result['translateResult'][0][0]['tgt']        #挑选出翻译后的字符串
    return changed
f = open('美国疫情.csv','r',encoding='utf-8') #mac不用这行，直接pd.read_csv(path)
data = pd.read_csv(f).astype(str)
record_num = int(data.describe().iloc[0,0])
f.close()
#建新csv文件
csvfile = open("美国疫情_clean.csv",'w',encoding='utf-8')
writer = csv.writer(csvfile)
writer.writerow(('username','date','review'))
#遍历出所有行的comment
for i in range(record_num):
    record = data.iloc[i,:]
    comment = record['review']
    comment = Translation(comment)          #将读取的每行review翻译为汉语
    comment = Chinese(comment)              #清洗一下翻译后的句子，只保留中文字符
    writer.writerow((record['username'],record['date'],comment))
csvfile.close()

# import pandas as pd
# import re
# from translate import Translator
# import csv
#
# def Chinese(text):      #处理函数
#     cleaned = re.findall(r'[\u4e00-\u9fa5]+', text)  #返回列表,用正则表达式筛选出中文
#     cleaned = ''.join(cleaned)                      #拼接成字符串
#     return cleaned
# def translateEtoC(text):
#     # 英语翻译中文
#     translator = Translator(to_lang="chinese")
#     translation = translator.translate(text)
#     return translation
# f = open('台湾疫情.csv','r',encoding='utf-8') #mac不用这行，直接pd.read_csv(path)
# data = pd.read_csv(f).astype(str)
# record_num = int(data.describe().iloc[0,0])
# #在循环中调用函数，对每行的comment操作，只保留中文字符
# for i in range(record_num):
#     record = data.iloc[i,:]
#     comment = record['review']
#     cleaned = Chinese(comment)
# f.close()
# #建新csv文件
# csvfile = open("台湾疫情_clean.csv",'w',encoding='utf-8')
# writer = csv.writer(csvfile)
# writer.writerow(('username','date','review'))
# #遍历出所有行的comment
# for i in range(record_num):
#     record = data.iloc[i,:]
#     comment = record['review']
#     comment = Chinese(comment)
#     writer.writerow((record['username'],record['date'],comment))
# csvfile.close()