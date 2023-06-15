#!/usr/bin/python

# -*- coding: utf-8 -*-

from init import *
from GetUrl import *
import pandas as pd
from urllib import parse
import os
import csv

class person:

    def __init__(self, name, information, occasion):
        self.name = name
        self.information = information
        self.occasion = occasion

list1 = []
list2 = []

hashmap1 = {}
hashmap2 = {}
hashmap3 = {}

def main():

    if not os.path.exists("./url.csv"):
        open("./url.csv", "w")
    if not os.path.exists("./keywords.csv"):
        open("./keywords.csv", "w")

    cnt1 = 0

    with open('./url.csv', 'rt', encoding='utf-8') as f:
        cr = csv.reader(f)
        for row in cr:
            tmp1 = list(row)
            if(len(tmp1) <= 0):
                continue
            hashmap1[tmp1[0]] = tmp1[0]
            hashmap3[tmp1[4]] = tmp1[4]
            cnt1 += 1
            print(cnt1)


    # 读入之前搜过的人，节省时间

    with open('./keywords.csv', 'rt', encoding='utf-8') as f:
        cr = csv.reader(f)
        for row in cr:
            tmp2 = list(row)
            if (len(tmp2) <= 0):
                continue
            hashmap2[tmp2[0]] = tmp2[0]

    cnt = 0

    # with open('./proxy.csv', 'rt', encoding='utf-8') as f:
    #     cr = csv.reader(f)
    #     for row in cr:
    #         tmp3 = list(row)
    #         if (len(tmp3) <= 0):
    #             continue
    #         list2.append(tmp3[0])
    #         cnt += 1

    cnt = 0
    tmpp = person([], [], [])
    with open("./list.txt", "r", encoding='utf-8') as f:
        for line1 in f:
            cnt += 1
            if(cnt % 3 == 1):
                tmpp = person([], [], [])
                tmpp.name = line1.split( )
            elif(cnt % 3 == 2):
                tmpp.information = line1.split( )
            else:
                tmpp.occasion = line1.split( )
                list1.append(tmpp)

    for i in list1:
        for j in i.name:
            for k in i.information:
                for l in i.occasion:
                    tmp1 = j
                    if(k != 'null'):
                        tmp1 += " " + k
                    if(l != 'null'):
                        tmp1 += " " + l
                    ff = 0
                    if(k == 'null' and l == 'null'):
                        ff = 1
                    print(tmp1)
                    uw = geturl(tmp1, hashmap1, hashmap2, i.name[0], list2, ff)
                    hashmap2[uw] = uw
                    df = pd.read_csv('./url.csv', header=None, engine='python')
                    le = len(df)
                    tmp4 = cnt1
                    for a in range(tmp4, le):
                        tmp2 = list(df.iloc[a])
                        if (len(tmp2) <= 0):
                            continue
                        hashmap1[tmp2[0]] = tmp2[0]
                        cnt1 += 1


    #with open('./keywords.csv', 'rt') as f:
    #    cr = csv.reader(f)
    #    for row in cr:
    #        tmp2 = list(row)
    #        if tmp2[3] in hashmap2:
    #            continue
    #        else:
    #            cr.

    df = pd.read_csv('./url.csv', header = None, engine='python')

    le = len(df)

    for i in range(0, le):
        tmp2 = list(df.iloc[i])
        if (len(tmp2) <= 0):
            continue
        if tmp2[4] in hashmap3:
            continue
        else:
            df.drop([i])
    '''
    理想的模式
    枚举所有人的关键字模式，发现这个组合已经被搜过，跳过
    已完成判断，只剩枚举
    一次搜完一组关键字的两页才存档一次
    
    还需要支持删除人物
    
    更远的任务
    处理好url准备下载
    预计需要ip池，但这个玩意从哪出呢
    '''

if __name__ == '__main__':
    main()