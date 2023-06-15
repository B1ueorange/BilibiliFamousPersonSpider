#!/usr/bin/python

# -*- coding: utf-8 -*-

import csv
from main import *

hashmap1 = {}
hashmap2 = {}

def init():

    # 导入之前的bv号，丢进个map里，确保不会重复使用
    with open('./url.csv', 'rt', encoding='utf-8') as f:
        cr = csv.reader(f)
        for row in cr:
            tmp1 = list(row)
            hashmap1[tmp1[0]] = tmp1[0]


    # 读入之前搜过的人，节省时间

    with open('./keywords.csv', 'rt', encoding='utf-8') as f:
        cr = csv.reader(f)
        for row in cr:
            tmp2 = list(row)
            hashmap2[tmp2[0]] = tmp2[0]

    # 读入需要读入的人员名单
    # 一个人应该有以下几种属性：姓名关键字 身份信息关键字 任务语境关键字
    # 每个关键字都应该占据一行