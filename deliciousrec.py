# -*- coding: utf-8 -*-
import pydelicious
import time
import recommendation


def initializeUserDictByTag(tag, count=5):
    user_dict = {}
    # 获取前count个最受欢迎的链接张贴记录
    for p1 in pydelicious.get_popular(tag=tag)[0:count] :
        # 查找所有张贴该链接的用户
        for p2 in pydelicious.get_urlposts(p1['url']) :
            user = p2['user']
            user_dict[user] = {}

    return user_dict

def initailizeUserDictByURL(url, count=5):
    user_dict = {}
    for urlposts in pydelicious.get_urlposts(url=url)[1 : count+1]:
        user = urlposts['user']
        user_dict[user] = {}

    return user_dict


def fillItems(user_dict) :
    all_items = {}
    # 查找所有用户都提价过的链接
    for user in user_dict:
        for i in range(3):
            try :
                posts = pydelicious.get_userposts(user)
                break
            except:
                print "Failed user " +user+ ", Retying."
                time.sleep(4)

        for post in posts:
            url = post['url']
            user_dict[user][url] = 1.0
            all_items[url] = 1.0

    # 用0填充缺失的项
    for ratings in user_dict.values() :
        for item in all_items:
            if item not in ratings :
                ratings[item] = 0.0



if __name__ == '__main__':
    user_dict = initailizeUserDictByURL('google.com')
    fillItems(user_dict)

    # {u'elenasoccer101': {}, u'bhavani2268': {}, u'sandwichman': {}, u'abnb34': {}}

    choose_use = 'elenasoccer101'






