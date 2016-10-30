# -*- coding: utf-8 -*-

import feedparser
import re

def getwordcounts(url):
    '''
    :param url:
    :return:  返回一个RSS订阅源的标题和包含单词计数情况的字典
    '''

    # 解析订阅源
    d = feedparser.parse(url)
    wc = {}

    # 循环遍历所有的文章条目
    for e in d.entries:
        if 'summary' in e :
            summary = e.summary
        else:
            summary = e.description

        # 提取单词列表
        words = getwords(e.title +' '+ summary)
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1

    return d.feed.title, wc


def getwords(html) :
    '''
    去除所有的HTML标签,并以非字母为分隔拆分出所有单词
    :param html:
    :return:
    '''
    txt = re.compile(r'<[^>]+>').sub('', html)
    words = re.compile(r'[^A-Z^a-z]+').split(txt)

    return [ word.lower() for word in words if word != '']


apcount = {}    # 单词在博客中出现的次数
blogwords = {} # 博客的单词频率

feedlist = [line for line in open('data/feed/feedlist.item')]

for feedurl in feedlist:
    if feedurl.startswith('#'):
        continue
    try :
        title, wc = getwordcounts(feedurl)
        blogwords[title] = wc
        for word, count in wc.items():
            apcount.setdefault(word, 0)
            if count > 0:
                apcount[word] += 1
    except:
        print 'Error URL: ', feedurl
        continue



# 选取介于 10% ~ 50%之间的单词
wordlist = []

for word, count in apcount.items():
    frac = float(count) / len(feedlist)
    if frac > 0.3 and frac < 0.5:
        wordlist.append(word)



out = file('out/blog.data', 'w')
out.write('Blog')
for word in wordlist:
    out.write('\t%s' % word)
out.write('\n')

for blog, wc in blogwords.items():
    out.write(blog)
    for word in wordlist:
        if word in wc :
            out.write('\t%d' % wc[word])
        else :
            out.write('\t0')
    out.write('\n')




