#!/usr/bin/python

# -*- coding: utf-8 -*-

import _thread
import multiprocessing
import os.path
import csv
import time
import face_recognition
import numpy as np
import subprocess
from PIL import Image

def ask1():
    frame_dir = './frame'
    frame_list = os.listdir(frame_dir)
    sum1 = 0
    sum2 = 0
    sum_1 = []
    sum_2 = []
    person_name = {}
    BV_list = {}
    name_list = []
    for i in range(0, 35):
        sum_1.append(0)
        sum_2.append(0)
    cnt = 0
    with open("./list.txt", 'rt', encoding='utf-8') as f:
        for line1 in f:
            cnt += 1
            if (cnt % 3 == 1):
                tmpp = line1.split()
                person_name[tmpp[0]] = int(cnt / 3)
                name_list.append(tmpp[0])
    with open('./url.csv', 'rt', encoding='utf-8') as f:
        cr = csv.reader(f)
        for row in cr:
            tmp3 = list(row)
            if (len(tmp3) <= 0):
                continue
            BV_list[tmp3[0]] = tmp3[4]

    for i in frame_list:
        point_name = frame_dir + '/' + i + '/gap.txt'
        if not os.path.exists(point_name):
            continue
        le = len(i)
        bv_name = ''
        fl = 0
        for j in range(0, le):
            if(i[j] == '['):
                bv_name = i[0:j]
                fl = 1
        if(fl == 0):
            bv_name = i
        if not BV_list.get(bv_name):
            continue
        le = len(os.listdir(frame_dir + '/' + i))
        tp0 = le - 6
        sum1 += le - 6
        sum_1[person_name[BV_list[bv_name]]] += tp0

    l = ''
    for i in name_list:
        l += i + ' ' + str(sum_1[person_name[i]]) + ' ' + str(sum_1[person_name[i]] / 3600) + 'h\n'

    l += '总和 ' + str(sum1) + ' ' + str(sum1 / 3600) + 'h '

    with open('./ZeroUse.txt', 'w', encoding='utf-8') as f:
        # f.writelines(str(sum1) + ' ' + str(sum2))
        f.write(l)

def main():

    ask1()

if __name__ == '__main__':
    main()