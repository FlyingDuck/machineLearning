# -*- coding: utf-8 -*-
import math
from PIL import Image, ImageDraw

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


def getheight(clust) :
    # 叶节点 高度为 1
    if clust.left == None and clust.right == None:
        return 1

    # 非叶子节点 高度为 分支节点高度之和
    return getheight(clust.left) + getheight(clust.right)

def getdepth(clust) :
    # 叶子节点的距离是 0.0
    if clust.left == None and clust.right == None:
        return 0.0

    # 非叶子节点的距离是 两个分支中距离较大者 + 节点本身距离
    return max(getdepth(clust.left), getdepth(clust.right)) + clust.distance

def drawdendrogram(clust, labels, jpeg="out/cluster.jpg") :
    # 高度和宽度
    h = getheight(clust)*20
    w = 1200
    depth = getdepth(clust)

    # 宽度固定,所以我们对距离进行相应的缩放
    scaling = float(w-150)/depth

    # 建立一个白色背景图片
    img = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.line((0, h/2, 10,h/2), (255, 0, 0))

    # 画第一个节点
    drawnode(draw, clust, 10, (h/2), scaling, labels)
    img.save(jpeg, 'JPEG')

def drawnode(draw, clust, x, y, scaling, labels) :
    if clust.id < 0 :
        h1 = getheight(clust.left)*20
        h2 = getheight(clust.right)*20
        top = y-(h1+h2)/2
        bottom = y+(h1+h2)/2

        ll = clust.distance * scaling

        draw.line((x, top+h1/2, x, bottom-h2/2), fill=(255, 0, 0))
        draw.line((x, top+h1/2, x+ll, top+h1/2), fill=(255, 0, 0))
        draw.line((x, bottom-h2/2, x+ll, bottom-h2/2), fill=(255, 0, 0))
        drawnode(draw, clust.left, x+ll, top+h1/2, scaling, labels)
        drawnode(draw, clust.right, x+ll, bottom-h2/2, scaling, labels)
    else:
        # 叶子节点 绘制节点的标签
        draw.text((x+5, y-7), labels[clust.id], (0,0,0))



blognames, words, data = readfile('out/blog.data')
clust = hcluster(data)

drawdendrogram(clust, blognames)