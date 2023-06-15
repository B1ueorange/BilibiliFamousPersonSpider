#!/usr/bin/python

# -*- coding: utf-8 -*-

from init import *
from GetUrl import *
import pandas as pd
from urllib import parse
import csv
import multiprocessing
import os.path
import time
import face_recognition
import numpy as np
import subprocess
from PIL import Image


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
            if (len(tmp1) <= 0):
                continue
            hashmap1[tmp1[0]] = tmp1[0]
            hashmap3[tmp1[4]] = tmp1[4]
            cnt1 += 1

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
            if (cnt % 3 == 1):
                tmpp = person([], [], [])
                if(cnt <= 210):
                    continue
                print(cnt / 3 + 1)
                tmpp.name = line1.split()
                tmp1 = face_recognition.load_image_file('./face/' + tmpp.name[0] + '.jpg')
                try:
                    personal_face_encoding = face_recognition.face_encodings(tmp1)[0]
                except Exception as e:
                    print(tmpp.name[0])
                if not os.path.exists('./face/' + tmpp.name[0] + '.jpg'):
                    print(tmpp.name)
            elif (cnt % 3 == 2):
                tmpp.information = line1.split()
            else:
                tmpp.occasion = line1.split()
                list1.append(tmpp)

    # with open('./keywords.csv', 'rt') as f:
    #    cr = csv.reader(f)
    #    for row in cr:
    #        tmp2 = list(row)
    #        if tmp2[3] in hashmap2:
    #            continue
    #        else:
    #            cr.



if __name__ == '__main__':
    main()