# -*- coding: utf-8 -*-
from math import sqrt

critics = {
    # Lisa Rose
    'Lisa': {
        'Lady': 2.5, 'Snake': 3.5, 'Luck': 3.0, 'Superman': 3.5, 'You': 2.5, 'Night': 3.0
    },
    # Gene Seymour
    'Gene': {
        'Lady': 3.0, 'Snake': 3.5, 'Luck': 1.5, 'Superman': 5.0, 'You': 3.5, 'Night': 3.0
    },
    # Michael Phillips
    'Michael': {
        'Lady': 2.5, 'Snake': 3.0,              'Superman': 3.5,             'Night': 4.0
    },
    # Claudia Puig
    'Claudia': {
                     'Snake': 3.5, 'Luck': 3.0, 'Superman': 4.0, 'You': 2.5, 'Night': 4.5
    },
    # Mick LaSalle
    'Mick': {
        'Lady': 3.0, 'Snake': 4.0, 'Luck': 2.0, 'Superman': 3.0, 'You': 2.0, 'Night': 3.0
    },
    # Jack Matthews
    'Jack': {
        'Lady': 3.0, 'Snake': 4.0,              'Superman': 5.0, 'You': 3.5, 'Night': 3.0
    },
    # Toby
    'Toby': {
                     'Snake': 4.5,              'Superman': 4.0, 'You': 1.0
    }
}

def sim_distance(prefs, person1, person2) :
    '''
    返回person1与person2基于距离的相似度评价
    :param prefs:       critics, 所有人的评论集合
    :param person1:     第一个人
    :param person2:     第二个人
    :return:            返回一个介于0~1之间的数,表示两人之间的相似度, 数值越大越相似
    '''
    # 获得两人都有评价的列表
    si = []
    for item in prefs[person1]:
        if item in prefs[person2]:
            si.append(item)

    # 如果两人没有共同评价, 返回0
    if len(si) == 0 :
        return 0

    # sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2) for item in prefs[person1] if item in prefs[person2]])
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2) for item in si])

    return 1/(1+sqrt(sum_of_squares))

def sim_pearson(prefs, person1, person2):
    '''
     返回person1和person2的皮尔逊相关系数, 皮尔逊相关系数是判断两组数据与某一直线拟合的一种度量, 采用这种方法可以修正"夸大分值"
    :param prefs:
    :param person1:
    :param person2:
    :return:
    '''
    # 挑选出双方都评价过的电影
    si = []
    for item in prefs[person1]:
        if item in prefs[person2]:
            si.append(item)

    n = len(si)

    if 0 == n:
        return 0

    # 对个人所有偏好求和
    sum1 = sum([prefs[person1][it] for it in si])
    sum2 = sum([prefs[person2][it] for it in si])

    # 对个人所有偏好求平方和
    sum1Sq = sum([pow(prefs[person1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[person2][it], 2) for it in si])

    # 求乘积之和
    pSum = sum([prefs[person1][it] * prefs[person2][it] for it in si])

    # 计算皮尔逊值
    num = pSum - (sum1*sum2/n)
    den = sqrt((sum1Sq - pow(sum1, 2)/n) * (sum2Sq - pow(sum2, 2)/n))

    if 0 == den:
        return 0

    return num/den


def topMatches(prefs, person, top=5, similarity=sim_pearson):
    '''
    从评价字典中计算与person最相似的top个匹配者
    :param prefs:
    :param person:
    :param top:
    :param similarity:
    :return:
    '''
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]

    # 对列表进行排序, 评价值最高的排在最前面
    scores.sort()
    scores.reverse()
    return scores[0: top]


def getRecommendation(prefs, preson, similarity=sim_pearson):
    '''
    利用其他人评价的加权平均, 为person推荐
    :param prefs:
    :param preson:
    :param similarity:
    :return:
    '''
    totals = {}
    simSums = {}
    for other in prefs:
        # 不需要和自己做比较
        if other == preson:
            continue
        sim = similarity(prefs, preson, other)

        # 忽略相似度不大于零的评价
        if sim <= 0 :
            continue

        # 计算每个人的加权评价值
        for item in prefs[other]:
            # 只对自己还未看过的影片进行评估
            if item not in prefs[preson] or prefs[preson][item] == 0:
                # 统计相似度之和
                simSums.setdefault(item, 0)
                simSums[item] += sim

                # 加权评价之和 (相似度 * 评价值)
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim

    rankings = [(total/simSums[item], item) for item, total in totals.items()]

    rankings.sort()
    rankings.reverse()
    return rankings



def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            result[item][person] = prefs[person][item]
    return result



def calculateSimilarItems(prefs, n=10) :
    result = {}
    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs :
        c += 1
        if c % 100 == 0 : print "%d / %d" % (c, len(itemPrefs))
        scores = topMatches(itemPrefs, item, n, similarity=sim_distance)
        result[item] = scores
    return result



def getRecommendedItems(prefs, itemMatch, user) :
    userRatings = prefs[user]
    scores = {}
    totalSim = {}

    for (item, rating) in userRatings.items() :
        for (similar, item2) in itemMatch[item] :
            if item2 in userRatings: continue
            scores.setdefault(item2, 0)
            scores[item2] += similar*rating

            totalSim.setdefault(item2, 0)
            totalSim[item2] += similar

    rankings = [ (score/totalSim[item], item) for item, score in scores.items()]

    rankings.sort()
    rankings.reverse()
    return rankings



def loadMovieLens(path='data/movielens') :
    movies = {}
    for line in open(path + '/movies.item'):
        if line.startswith('#'): continue
        (id, name) = line.split(',')[0:2]
        movies[id] = name

    prefs = {}
    for line in open(path + '/ratings.item'):
        if line.startswith('#'): continue
        (userId, movieId, rating) = line.split(',')[0:3]
        prefs.setdefault(userId, {})
        prefs[userId][movies[movieId]] = float(rating)

    return prefs




if __name__ == '__main__':
    # print "欧几里得距离: " , sim_distance(critics, 'Lisa', 'Gene')
    # print "皮尔逊系数: ", sim_pearson(critics, 'Lisa', 'Gene')

    # print "最佳匹配者By sim_distance: " , topMatches(critics, 'Toby', 5, sim_distance)
    # print "最佳匹配者By sim_pearson: " , topMatches(critics, 'Toby', 5, sim_pearson)

    # print "推荐影片: ", getRecommendation(critics, 'Toby', sim_pearson)

    movies = transformPrefs(critics)
    print "最佳匹配影片: ", topMatches(movies, 'Superman', 5, sim_pearson)