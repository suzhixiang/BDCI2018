#coding=utf-8

import pandas as pd

import jieba
import numpy as np
raw=pd.read_csv("test_public.csv")
content=raw["content"]
subject_dic= \
    {'优惠': 1, '车价': 1, '獠牙': 5, '后备箱': 8, '方向盘': 6, '车身': 5, '外观': 5, '做工': 2, '安全性': 4, '刹车灯': 4, '轴承': 3, '全时': 6,
     '安卓': 3, '雷达': 3, '加速': 10, '价格': 1, '空间': 8, '省油': 7, '刹车盘': 4, '影像': 3, '风噪': 9, '操控': 6, '座椅': 2, '动力': 10,
     '舒适性': 9, '好看': 5, '异响': 9, '消耗': 10, '变速箱': 10, '尾灯': 5, '材料': 2, '油耗': 7, '底盘': 6, '发动机': 10, '车漆': 5, '刹车片': 4,
     '导航': 3, 'abs': 4, '内饰': 2, '颜色': 5, '中控': 3, '刹车': 4, '操控性': 6, '配置': 3, '噪音': 9, '气囊': 4, '空调': 9, '性能': 6,
     '前脸': 5, '刹车油': 4}
standard_sub=["价格","价格","内饰","配置","安全性","外观","操控","油耗","空间","舒适性","动力"]
subject_contains=[]
for i in range(len(content)):
    subject_contains.append(np.zeros(11,dtype=np.int).tolist())
    for sub in subject_dic:
        num=content.values[i].count(sub)
        subject_contains[i][subject_dic[sub]]+=num
result=[]
num2=0
for i in range(len(content)):
    num=0
    for j in range(len(standard_sub)):
        if(subject_contains[i][j]>0):
            result.append([raw["content_id"].values[i],standard_sub[j],0,None])
            num+=1
    if(num==0):
        result.append([raw["content_id"].values[i],standard_sub[0],0,None])
result=pd.DataFrame(result)
result.columns=["content_id","subject","sentiment_value","sentiment_word"]
result["sentiment_value"]=result["sentiment_value"].astype(int)
result.to_csv("result.csv",encoding="UTF-8",index=False)