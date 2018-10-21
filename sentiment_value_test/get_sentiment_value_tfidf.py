# coding=gbk
import pandas as pd
import torch
import numpy as np
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer

raw = pd.read_csv("result_tfidf1.csv")
content_id = raw["content_id"]
content2 = raw["content"]
subject = raw["subject"]
sentiment_value = raw["sentiment_value"]
subject_dic = {"价格": 0, "内饰": 1, "配置": 2, "安全性": 3, "外观": 4, "操控": 5, "油耗": 6, "空间": 7, "舒适性": 8, "动力": 9}
key_words = \
    ['结实', '5w40', '92', '合适', '增加', '价格便宜', '市区', '德系', '车型', '油耗', '30', '随叫随到', '器材', '屏幕', '主打', '塑料', '整体', '国产',
     '欧蓝德', '拉风', '上要', '人比', '大气', '略贵', '贵不说', '前排', '大是', '品牌', '满意', '足点', '消耗', '吊打', 'fb', '尺寸', '比较稳定', '老车',
     '评都', '急刹', '便利性', '前档', '国籍', '安卓', '静音', '排量', '召回', '不错', '硬点', '广东', '太硬', '东西', '不高', '事件', '要命', '劲畅', '投诉',
     '驱能', '尾灯', '上泵', '不太爽', '感高', '舒适', '优点', '装甲', '12', '舒适性', '后排', '无感', '小贵', '要说', '原装', '强劲', '好看', '顺利', '四驱',
     '汉兰达', '老气', '配件', '人好', '石子', '当当', '一点', 'xv', '全时', '汽油', '前脸', '音质', '26', '黑屏', '过年', '庞大', '11', '时尚', '精致',
     '25000', '点刹', 'ej', '车漆能', '不买', '好意思', '城市', '看上', '偷工减料', '饰板', '垃圾', '略低', '车中', '我加', '风噪大', '用料', '视野',
     '刹车油', '开着', '持竖屏', '豪车', '不值', '喜欢', '比率', '隔音', '款式', '最低', '起步', '操控性', '格叽格', '科技', '太丑', '不太', 'kg', '舒适度',
     '在内', '没换', '人四驱', '给力', '对小森', '小熊', '贵皮', '我试', '坐上去', '豪华', '差点', '主用', '4s店', '后座', '很漂亮', '配置', '机头', '硬伤',
     '理想', '不合', '夏天', '手动', '拼凑', '一众', '光大', '急刹车', '风险', '启停', '新换', 'edfc', '支臂', 's3', '感觉', '四区', '瞬时', '森林',
     '奇丑无比', '死硬', '杀马特', '水平', '舒服', '新款', '过高', '分享', '没后', '高度', '过时', '出身', '发动机', '玻璃', '广州', '出风口', '轴距', '侧重',
     '震动', '太小', '红绿灯', '爱车', '刚换', '认可度', '不底', '四十米', '更让人', '车载', '一股', '铺装', '越野', '综合', '冷车', '省油', '第三方', '线性',
     '不低', '三条', '距离', '率低', '发烧', '爆震', '超级', '高车', '维修', '奇怪', '高点', '逼格', '日系', '拆过', '太高', '15w', '担心', '车衣', '指南',
     '护板', '不减', '奇骏', '金属', '厉害', '人强', '优势', '出风', 'app', '百万', '比森整', '颜色', '安全性', '算是', '解决', '130', '停机', '百公里',
     '手机', '密封', '上浮', '焦糊', '偏硬', '尊贵', '补充', '比白桶', 'l0w', '大屏幕', '轿车', '足够', '翻天', '空调', '畸形', '漆软', 'rav4', '变速箱',
     '循环', '降到', '冲着', '完败', '优越', '会贵', '实惠', '规车', '暖和', '造型', '刹车踏板', '眼缘', '13', '摆动', '故障率', '报废', '恶心', '山寨',
     '记录', '能比', '下降', '省十来', '偏高', '保养', '方向', '滞后', '进口车', '油门', '乘坐', '面上', '加四驱', 'q5', '够用', '低风阻', '感谢', '设计',
     '14', '探界者', '公路', '平均', '寒酸', '啸叫', '音响', '很小', '说实话', '人差', '大视野', '大车', '提升', '做工', '差强人意', '更好', '对置', '甩奇',
     '纸壳', '08', '气囊', '按钮', '力量', '虚高', '重心', '臭味', '冻住', '铝合金', '10', '好点', '森烧', '0w40', '加热', '倒车', '比前', 'suv',
     '个头', '帕杰罗', '加速', '坚挺', '不差', '傲虎', '前段', '很大', '车漆', '缺陷', '95', '大改', '减少', 'q8', '轴承', '年轻', '丈母娘', '车重', '自费',
     '身份', '太贵', '简陋', '性价比', '顶棚', '乱入', 'xt', '省心', '16', '叽响', '座椅', '全系', '再贵', '森大', '材质', '不烧', '车内', '反馈', '公里',
     '热心', '维特', '坏过', '难看', '真皮', '二手车', '多丑', '牛逼点', '纵置', '超车', '提高', '特别', '森好', '漆好', '强奸', '13xt', '启动', '20',
     '便宜', '过余', '上均', '壳子', '万能', '漂亮', '驾小森', '好些', '德味', '困扰', '100km', '管子']

temp = pd.read_csv("tf_idf.csv", encoding="gbk")
standard_sub = ['价格-1', '价格0', '价格1', '内饰-1', '内饰0', '内饰1', '配置-1', '配置0', '配置1', '安全性-1', '安全性0', '安全性1', '外观-1',
                '外观0', '外观1', '操控-1', '操控0', '操控1', '油耗-1', '油耗0', '油耗1', '空间-1', '空间0', '空间1', '舒适性-1', '舒适性0', '舒适性1',
                '动力-1', '动力0', '动力1']

words_tfidf = temp[key_words]
values = [[] for i in range(len(raw))]
for i in range(len(raw)):
    for j in range(30):
        v = 0
        words = jieba.lcut(raw["content"].values[i])
        for word in words:
            if (word in words_tfidf.columns.tolist()):
                v += words_tfidf[word].values[j]
        values[i].append(v)
values = pd.DataFrame(values)
values.columns = standard_sub
data = []
for i in range(len(values)):
    sum = 0
    for j in range(len(values.values[i])):
        sum += values.values[i][j]
    for j in range(len(values.values[i])):
        values.values[i][j] /= sum
values.to_csv("values.csv",encoding="UTF-8")


def get_accuracy(threshold=0.62):
    subject_contains = []
    T=0
    i = 0
    while (i < len(content2)):
        index=0
        value=0
        for j in range(len(values.values[i])):
            if(values.values[i][j]>value):
                value=values.values[i][j]
                index=j%3-1
        if value<threshold:
            index=0
        if index==sentiment_value[i]:
            T+=1
        i+=1
    P=T/len(content2)
    return P

#values=pd.read_csv("values.csv",encoding=UTF-8)
cp = values.copy()
for j in range(1, 100):
    values = cp.copy()
    print(get_accuracy(0.01*j), j)
