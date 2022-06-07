# coding: utf-8
import pandas as pd

import jieba
import time

def txt_cut(juzi):
    return [w for w in jieba.lcut(juzi) if w not in stop_list]     #可增长len(w)>1


def emotion_caculate(text):
    positive = 0
    negative = 0
    anger = 0
    disgust = 0
    fear = 0
    sad = 0
    surprise = 0
    good = 0
    happy = 0

    wordlist = txt_cut(text)
    # wordlist = jieba.lcut(text)
    wordset = set(wordlist)
    wordfreq = []
    for word in wordset:
        freq = wordlist.count(word)
        if word in Positive:
            positive += freq
        if word in Negative:
            negative += freq
        if word in Anger:
            anger += freq
        if word in Disgust:
            disgust += freq
        if word in Fear:
            fear += freq
        if word in Sad:
            sad += freq
        if word in Surprise:
            surprise += freq
        if word in Good:
            good += freq
        if word in Happy:
            happy += freq

    emotion_info = {
        'length': len(wordlist),
        'positive': positive,
        'negative': negative,
        'anger': anger,
        'disgust': disgust,
        'fear': fear,
        'good': good,
        'sadness': sad,
        'surprise': surprise,
        'happy': happy,

    }

    indexs = ['length', 'positive', 'negative', 'anger', 'disgust', 'fear', 'sadness', 'surprise', 'good', 'happy']
    return pd.Series(emotion_info, index=indexs)

#获取数据集
f = open('美国疫情_clean.csv',encoding='utf8')
weibo_df = pd.read_csv(f).astype(str)
#print(weibo_df.head())
# 扩展前的词典
df = pd.read_excel('大连理工大学中文情感词汇本体NAU.xlsx')
#print(df.head(10))

df = df[['词语', '词性种类', '词义数', '词义序号', '情感分类', '强度', '极性']]
#df.head()
Happy = []
Good = []
Surprise = []
Anger = []
Sad = []
Fear = []
Disgust = []
#df.iterrows()功能是迭代遍历每一行
for idx, row in df.iterrows():
    if row['情感分类'] in ['PA', 'PE']:
        Happy.append(row['词语'])
    if row['情感分类'] in ['PD', 'PH', 'PG', 'PB', 'PK']:
        Good.append(row['词语'])
    if row['情感分类'] in ['PC']:
        Surprise.append(row['词语'])
    if row['情感分类'] in ['NB', 'NJ', 'NH', 'PF']:
        Sad.append(row['词语'])
    if row['情感分类'] in ['NI', 'NC', 'NG']:
        Fear.append(row['词语'])
    if row['情感分类'] in ['NE', 'ND', 'NN', 'NK', 'NL']:
        Disgust.append(row['词语'])
    if row['情感分类'] in ['NAU']:     #修改: 原NA算出来没结果
        Anger.append(row['词语'])

#正负计算不是很准 本身能够制定规则
Positive = Happy + Good + Surprise
Negative = Anger + Sad + Fear + Disgust
print('情绪词语列表整理完成')
print(Anger)

#添加使用者词典和停用词
jieba.load_userdict("user_dict.txt")              #自定义词典
stop_list = pd.read_csv('stop_words.txt',
                        engine='python',
                        encoding='utf-8',
                        delimiter="\n",
                        names=['t'])['t'].tolist()

#---------------------------------------情感分析---------------------------------
start = time.time()
emotion_df = weibo_df['review'].apply(emotion_caculate)
end = time.time()
print("共耗时：",end-start)
print(emotion_df.head())            #输出头部五条数据
print("ok")
#输出结果
output_df = pd.concat([weibo_df, emotion_df], axis=1)
output_df.to_csv('美国疫情TTtest.csv',encoding='utf_8_sig', index=False)
#print(output_df.head())
