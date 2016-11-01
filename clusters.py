# -*- coding: utf-8 -*-
import math

def readfile(filename) :
    lines = [line for line in file(filename)]

    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:] :
        p = line.strip().split('\t')
        rownames.append(p[0])
        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data


def pearson(v1, v2) :
    # 简单求和
    sum1 = sum(v1)
    sum2 = sum(v2)

    # 求平方和
    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])

    # 求乘积和
    pSum = sum([v1[i]*v2[i] for i in range(len(v1))])

    # 计算 pearson score
    num = pSum - (sum1 * sum2/len(v1))
    den = math.sqrt((sum1Sq - pow(sum1, 2)/len(v1))*(sum2Sq - pow(sum2, 2)/len(v2)))
    if 0 == den:
        return 0

    return 1.0 - num/den


class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.distance = distance
        self.id = id


def hcluster(rows, distance=pearson) :
    distances = {}
    currentclusterid = -1

    clust = [bicluster(vec=rows[i], id=i) for i in range(len(rows))]

    while len(clust) > 1:
        # 记录当前最小距离 及其 位置
        lowestpair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)

        #  遍历每一个配对,寻找最小距离
        for i in range(len(clust)) :
            for j in range(i+1, len(clust)) :
                # 用distances 缓存距离
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)

                d = distances[(clust[i].id, clust[j].id)]
                if d < closest :
                    closest = d
                    lowestpair = (i, j)

        # 计算两个聚类的平均值
        mergevec = [
            (clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i])/2.0
            for i in range(len(clust[0].vec))
        ]

        # 建立新的聚类
        newcluster = bicluster(mergevec,
                               left=clust[lowestpair[0]],
                               right=clust[lowestpair[1]],
                               distance=closest,
                               id=currentclusterid)

        currentclusterid -= 1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    return clust[0]


def printclust(clust, labels=None, n=0) :
    # 利用缩进来建立层级布局
    for i in range(n):
        print ' ',

    if clust.id < 0 :
        print '-'
    else:
        if labels==None:
            print clust.id
        else :
            print labels[clust.id]

    if clust.left != None:
        printclust(clust.left, labels=labels, n = n+1)
    if clust.right != None:
        printclust(clust.right, labels=labels, n= n+1)