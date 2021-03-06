# coding=gbk
import pandas as pd
import torch
import numpy as np
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer

raw = pd.read_csv("../train.csv")
content_id = raw["content_id"]
content2 = raw["content"]
subject = raw["subject"]
sentiment_value = raw["sentiment_value"]
subject_dic = {"价格": 0, "内饰": 1, "配置": 2, "安全性": 3, "外观": 4, "操控": 5, "油耗": 6, "空间": 7, "舒适性": 8, "动力": 9}
key_words = \
    ['ok', '一流', '一点点', '一般般', '下不来', '下机油', '下降', '下降明显', '不严实', '不介意', '不会便宜', '不会后悔', '不会小', '不会很快', '不会高', '不佳', '不便宜', '不值', '不值得', '不值钱', '不公平', '不协调', '不可能低', '不合算', '不合适', '不后悔', '不咋地', '不咋新潮', '不咋样', '不喜欢', '不在乎', '不在意', '不够整', '不够用', '不太喜欢', '不太行', '不太重视', '不好', '不好受', '不好看', '不如之前', '不如现款', '不完善', '不实用', '不小', '不少机油', '不差', '不带导航', '不强', '不感冒', '不擅长', '不支持', '不改改', '不敢恭维', '不方便', '不满意', '不漏', '不烧', '不烧机油', '不省油', '不着调', '不符合', '不算问题', '不纠结', '不细致', '不给力', '不耐磨', '不能忍', '不能接受', '不能比拟', '不能比的', '不舒坦', '不舒服', '不菲', '不行', '不见得省', '不解释', '不豪华', '不贵', '不费劲', '不选', '不逊于', '不错', '不错不错', '不错的', '不靠谱', '不飘', '不高', '专业', '中上游', '中庸', '中控山寨', '中控差', '中等', '中网丑', '乘客舒适', '也不错', '也不高', '也贵', '乱响', '亲民点', '仍觉得好', '代价大', '令人发指', '价差很大', '价格一般', '价格不够', '价格不错', '价格太贵', '价格好', '价格贵', '价格较高', '价格过高', '价格还行', '价格高', '优势', '优势明显', '优惠', '优惠不错', '优惠太小', '优惠小', '优点', '伤感情', '伤蓄电池', '低调', '作用不大', '便宜', '便宜些', '便宜很多', '保值耐用', '信心满满', '值得', '值得拥有', '倾斜大', '偏了', '偏低', '偏大', '偏弱', '偏硬', '偏磨', '做工好', '做工粗糙', '充足', '全塑料', '全时四驱', '内饰一般', '内饰低档', '内饰改改', '内饰简陋', '内饰要吐', '内饰豪华', '冒烟了', '冻得', '减少', '出毛病', '出色', '出问题', '分区空调', '别奢望', '别指望', '别提了', '别纠结', '制冷快', '刹不住', '刹车盘', '刹车软', '刺拉拉', '前脸好看', '前脸无爱', '加热', '加速不错', '加速好点', '加速快', '加速抖动', '加速缓慢', '动力下降', '动力不够', '动力不行', '动力不足', '动力不错', '动力为王', '动力呵呵', '动力够用', '动力好点', '动力弱', '动力强多', '动力更好', '动力牛', '动力足', '升级', '升高', '单价高', '单调', '卡死', '卡顿', '厉害', '压力大', '厚道', '原厂', '参差不齐', '又硬又凸', '反应慢', '反应敏捷', '发出声音', '取消', '受不了', '变冰箱', '变大', '变弱', '变色', '变速箱差', '变闷', '只优惠', '可以了', '可以保持', '可以忽略', '可以的', '可以调节', '可靠', '各种响', '合理就行', '合眼缘', '合适', '合适就买', '吊打', '后备箱大', '后悔', '后排挤', '后段不行', '后窗', '吐槽', '告诉抖动', '味特别大', '咬咬牙的', '品质不错', '哗啦声', '哪个贵', '唯一不足', '啥都好', '喜欢', '嘎嘎响', '噪音', '噪音下降', '噪音不大', '噪音低', '噪音依旧', '噪音偏大', '噪音减少', '噪音变大', '噪音大', '噪音小', '噪音很小', '噪音较大', '四驱旅行', '四驱无敌', '国内减配', '土腥味', '在意', '均衡', '坐姿高', '坑爹', '垃圾', '垃圾导航', '基本可以', '堪比跑车', '增加', '增加油耗', '声音低沉', '声音变小', '声音大', '声音很大', '外形好看', '外观不错', '外观太丑', '多丑', '多余的', '够了', '够可以', '够用', '大不少', '大了很多', '大些', '大改', '大气', '大空间', '大致相同', '太吵', '太垃圾', '太好了', '太小', '太小了', '太差', '太弱', '太扯了', '太水', '太稳了', '太给力了', '太贵了', '太高', '失望', '奇高', '套路', '好一些', '好不少', '好了很多', '好些', '好像', '好动力', '好听', '好太多', '好开', '好很多', '好很很多', '好性能', '好感', '好点', '好用', '好的多', '好看', '好难看', '安心', '安静', '完全够用', '完美', '完胜', '完败', '实惠', '实用', '容量大', '宽大舒适', '宽敞', '对口味', '尊贵', '小一点', '小了点', '小贵', '就别想了', '尾灯好丑', '山寨', '差些', '差别明显', '差劲', '差多了', '差很多', '差很远', '差点', '差点意思', '差点追尾', '差距不大', '已成绝唱', '市区', '布局限制', '帅气', '带喜感', '干净', '平庸', '平衡', '平顺自然', '底盘厉害', '底盘更高', '底盘最高', '底盘漏油', '底盘高', '废刹车', '废油', '座椅臭味', '廉价', '开着爽', '开着累', '异味', '异响', '异响多', '弱了点', '强些', '强劲', '强化', '强太多', '强很多', '强点', '影响', '影响散热', '影响驾驶', '很一般', '很不错', '很低', '很冷', '很准', '很危险', '很喜欢', '很够用', '很好', '很好用', '很差', '很满意', '很漂亮', '很烦', '很爽', '很稳', '很耐看', '很舒适', '很良心', '很韧性', '很高', '心寒', '心理没底', '忍住没改', '忽略不计', '急刹车', '急加速', '性价比', '性价比低', '性价比高', '性能好', '性能强', '恒温', '恼人', '惊喜', '惨不忍睹', '愉快', '感觉不到', '感觉不错', '手感不错', '手感差', '手感爆炸', '手机导航', '才优惠', '才叫车', '打60分', '打80分', '打95分', '扯淡', '承受不起', '抓狂', '抖动', '抖抖', '护板破碎', '担心', '担心不足', '拔尖', '挫样', '挺大', '挺好的', '挺棒', '挺炫', '挺省油的', '挺稳的', '挺高', '捉急', '换代慢', '换油', '掉了链子', '掉渣', '掉漆', '排量大', '接受不了', '控制不了', '掩盖噪音', '掰不动', '提升', '提升太多', '提速', '提速快', '提速满意', '提高', '提高很多', '摆动', '摇晃', '摩擦音', '操控不错', '操控也好', '操控好', '操控很棒', '操控感', '操控满意', '改观不少', '放弃', '故障', '效果不错', '断轴', '方向盘飘', '无力吐槽', '无变化', '无奈', '无所谓', '无损耗', '无敌', '无毛病', '无法比', '无解', '早日完蛋', '时尚', '是否可以', '是大的', '是好车', '显小', '更吵', '更好', '更强', '更扎实', '更方便', '更硬', '更足', '更高', '最适合', '有些粗', '有优势', '有保障', '有动力', '有变化', '有味', '有啥用', '有噪音', '有声音', '有异响', '有所下降', '有所提升', '有提升', '有效果', '有点土', '有点小', '有点影响', '有点性能', '有点抖', '有点提升', '有点糙', '有点降低', '有点难受', '有缺点', '有钱任性', '有问题', '有面子', '机油不好', '机油消耗', '杀手锏', '杠杠的', '松垮', '查不出', '欠缺', '正常价格', '正常保养', '死硬', '毁所有', '比不上', '比不了', '比不过', '比以前多', '比以前快', '比较低的', '比较合理', '比较好', '比较差', '比较灵', '毛病多', '气味呛人', '没事', '没优势', '没关系', '没动力', '没区别', '没啥优惠', '没啥区别', '没增加', '没宽敞', '没得比', '没得说', '没必要', '没必要做', '没情况', '没感觉', '没戏', '没敢玩', '没有优势', '没有保证', '没有导航', '没有磨损', '没有问题', '没法比', '没烧', '没用', '没的说', '没落锁', '没那么好', '没问题', '油耗上升', '油耗下降', '油耗低', '油耗增加', '油耗大', '油耗太高', '油耗好', '油耗很高', '油耗造假', '油耗高', '涉水', '渗油', '渣渣', '温度高', '滋滋声', '满意', '滴水现象', '漂亮', '漂移', '漆面太薄', '漏油', '灵巧', '灵敏', '灵活', '烧机油', '熄火', '爆缸', '爆震', '牛b了', '牛车', '牛逼', '特别抖', '特别迷恋', '特大', '理想', '生猛', '生锈', '用处不大', '用料不错', '用的很好', '甩n条街', '甩三条街', '略胜一筹', '略贵', '略高', '疯狂', '皮实', '皮实耐用', '相当不错', '相当好', '相当棒', '相当给力', '省心', '省油', '省油的', '省钱', '看不上眼', '看中外观', '真不喜欢', '真的不错', '真的是', '真难看', '真高', '着迷', '知足', '破百', '硬伤', '硬朗', '确实不好', '确实好', '确实很棒', '确实省', '磕碜了点', '磨得发亮', '磨损', '秀气', '秒杀', '稍微高点', '稳定', '空调', '空调问题', '空间不小', '空间不行', '空间也大', '空间大', '空间更大', '空间有点', '空间舒适', '空间较大', '符合', '第一', '简单', '简洁干练', '简约的很', '简陋', '算我输', '粗糙', '紧凑', '纠结', '结实', '给力', '绝对值', '缺失遗憾', '缺陷', '老坏', '老气', '老牛逼', '耐用', '肯定', '肯定烧', '背光', '胜出', '能比', '脱皮', '腰疼', '自信多了', '舒服', '舒服安静', '舒服的很', '舒适感强', '落后', '虚高', '蛮好', '行情价', '要求一致', '规格', '视野好', '认可度高', '记忆', '设计缺陷', '豪华感强', '负担大', '败笔', '质量不行', '质量好', '质量很差', '贵一点', '贵了', '贵太多', '费油', '费用不高', '贼高', '超前', '超好用', '超车', '超过', '越丑', '足够', '足够了', '距离短', '跟不上', '车体高', '车挺好', '车漆真软', '车漆薄', '车漆软', '车重', '转速低', '轰轰响', '轻微渗油', '轻松', '轻盈', '较好', '较小', '较差', '过时', '运气好', '还不如', '还不错', '还便宜', '还可以', '还好', '还得', '还行', '还行吧', '还过的去', '连线', '追不上', '追求', '适当保养', '逊色', '通病', '逼格高', '郁闷', '都一样', '都不错', '都行', '配置简陋', '配置高', '醉了', '里外不一', '重一点', '重心低', '重新打胶', '钻进去', '锁死', '问题不大', '闻名', '降了', '降低', '降低动力', '随叫随到', '随性', '隔音不好', '隔音太差', '隔音差', '难受', '难点', '难看', '静音', '静音不好', '静音舒适', '非常一般', '非常不错', '非常好', '非常满意', '非常猛', '面包车', '音响太差', '音质不行', '顶不住', '顶级', '颇高', '颜值差', '颜值高', '额外惊喜', '颠簸', '风力强劲', '风噪大', '风噪最大', '风险很大', '飙车差劲', '飞叉叉', '驾驶', '高一点', '高了', '高了好多', '高了点', '高大上', '高很多', '高昂', '高点', '高配好看', '鸡肋', '黑屏', '齐全就行']

temp = pd.read_csv("sentiment_words_tf_idf.csv", encoding="gbk")
standard_sub = [-1,0,1]
for word in key_words:
    if(word.count("不") == 0):
        jieba.add_word("不" + word)
    else:
        jieba.add_word(word)
words_tfidf = temp[key_words]
values = [[] for i in range(len(raw))]
for i in range(len(raw)):
    for j in range(len(standard_sub)):
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
values.to_csv("words_values.csv",encoding="UTF-8")


def get_accuracy(threshold=0.32):
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
print(get_accuracy(1.01), 101)
for j in range(1, 100):
    values = cp.copy()
    print(get_accuracy(0.01*j), j)
