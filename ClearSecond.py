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
import pytorch_ssim
import torch
import torchvision
import torch.autograd

def get_num(x):
    if (x >= 10000):
        return str(x)
    if (x >= 1000):
        return '0' + str(x)
    if (x >= 100):
        return '00' + str(x)
    if (x >= 10):
        return '000' + str(x)
    if (x >= 1):
        return '0000' + str(x)

def Ssim(img_path1_1, img_path2_2):
    # img1=keras.preprocessing.image.load_img(img_path1_1)  #先通过keras读取图片，
    # img1_array=keras.preprocessing.image.img_to_array(img1)/255   #将图片转换为数组
    #
    # img2=keras.preprocessing.image.load_img(img_path2_2)
    # img2_array=keras.preprocessing.image.img_to_array(img2)/255


    img1 = torch.autograd.Variable(torchvision.transforms.ToTensor()(Image.open(img_path1_1)))
    img2 = torch.autograd.Variable(torchvision.transforms.ToTensor()(Image.open(img_path2_2)))

    img1 = img1.unsqueeze(0)
    img2 = img2.unsqueeze(0)
    if torch.cuda.is_available():
        img1 = img1.cuda()
        img2 = img2.cuda()

    sim=float(pytorch_ssim.ssim(img1, img2))
    # mse=measure.compare_mse(img1_array,img2_array)
    return sim


def clearsecond(bv_name, p_name):
    # if os.path.exists('./frameSecond/' + p_name + '/' + bv_name + '/FinishClear.txt'):
    #     return
    if not os.path.exists('./frameSecond/' + p_name + '/' + bv_name):
        os.makedirs('./frameSecond/' + p_name + '/' + bv_name)
    if not os.path.exists('./frame/' + bv_name + '/FinishFfmpeg.txt'):
        with open('./frameSecond/' + p_name + '/' + bv_name + '/FinishClear.txt', 'w', encoding='utf-8') as f:
            f.writelines('emmmmm')
        return
    le = len(os.listdir('./frame/' + bv_name))
    num = 0
    with open('./frame/' + bv_name + '/gap.txt', 'rt', encoding='utf-8') as f:
        for line in f:
            tmp1 = line.split( )
            num += (int(tmp1[1]) - int(tmp1[0]))
    print(bv_name)
    print(num / (le - 7))
    if(num / (le - 7) <= 0.300000):
        with open('./frameSecond/' + p_name + '/' + bv_name + '/FinishClear.txt', 'w', encoding='utf-8') as f:
            f.writelines('emmmmm')
        return
    flag = []
    flag1 = []
    flag2 = []
    flag3 = []
    for i in range(0, le):
        flag.append(0)
        flag1.append(0)
        flag2.append(0)
        flag3.append(1)
    with open('./frame/' + bv_name + '/point.txt', 'rt', encoding='utf-8') as f:
        for line in f:
            tmp1 = line.split( )
            flag[int(tmp1[0])] = 1
    with open('./frame/' + bv_name + '/deformation.txt', 'rt', encoding='utf-8') as f:
        for line in f:
            tmp1 = line.split( )
            ch = float(tmp1[2])
            if(ch < 0.665899 or ch > 1.49661):
                flag1[int(tmp1[1])] = 0
            else:
                flag1[int(tmp1[1])] = 1
    with open('./frame/' + bv_name + '/move.txt', 'rt', encoding='utf-8') as f:
        for line in f:
            tmp1 = line.split( )
            ch = float(tmp1[4])
            pp = int(tmp1[1])
            if(ch >= 0.20000):
                if(ch >= 0.350000):
                    flag2[int(tmp1[1])] = 0
                elif(Ssim('./frame/' + bv_name + '/' + get_num(pp) + '.jpg', './frame/' + bv_name + '/' + get_num(pp - 1) + '.jpg') <= 0.6800000):
                     flag2[int(tmp1[1])] = 0
                else:
                    flag2[int(tmp1[1])] = 1
            else:
                flag2[int(tmp1[1])] = 1
    with open('./frame/' + bv_name + '/area.txt', 'rt', encoding='utf-8') as f:
        for line in f:
            tmp1 = line.split( )
            if(float(tmp1[2]) <= 0.0180000000):
                flag3[int(tmp1[1])] = 0
    fl1 = 0
    s = ''
    l = 0
    for i in range(1, le - 6):
        if(flag[i] == 1):
            if(fl1 == 0):
                fl1 = 1
                l = i
            elif(flag1[i] == 0 or flag2[i] == 0 or flag3[i] == 0):
                s += str(l) + ' ' + str(i - 1) + '\n'
                l = i
                # if(bv_name == 'BV13x411k7dB'):
                #     print(str(i) + ' ' + str(flag1[i]) + ' ' + str(flag2[i]) + ' ' + str(flag3[i]))
        else:
            if(fl1 == 1):
                fl1 = 0
                s += str(l) + ' ' + str(i - 1) + '\n'
                # if (bv_name == 'BV13x411k7dB'):
                #     print(str(i) + ' ' + str(flag1[i]) + ' ' + str(flag2[i]) + ' ' + str(flag3[i]))
    if(fl1 == 1):
        s += str(l) + ' ' + str(le - 7) + '\n'
    with open('./frameSecond/' + p_name + '/' + bv_name + '/gap.txt', 'w', encoding='utf-8') as f:
        f.writelines(s)
    with open('./frameSecond/' + p_name + '/' + bv_name + '/FinishClear.txt', 'w', encoding='utf-8') as f:
        f.writelines('emmmmm')

def cs():
    cnt = 0
    name_list = []
    BV_list = {}
    person_name = {}
    with open("./list.txt", 'rt', encoding='utf-8') as f:
        for line1 in f:
            cnt += 1
            if (cnt % 3 == 1):
                tmpp = line1.split()
                person_name[tmpp[0]] = int(cnt / 3)
                name_list.append(tmpp[0])
                if(not os.path.exists('./frameSecond/' + tmpp[0])):
                    os.makedirs('./frameSecond/' + tmpp[0])
    with open('./url.csv', 'rt', encoding='utf-8') as f:
        cr = csv.reader(f)
        for row in cr:
            tmp3 = list(row)
            if (len(tmp3) <= 0):
                continue
            BV_list[tmp3[0]] = tmp3[4]
    frame_list = os.listdir('./frame')
    for i in frame_list:
        le = len(i)
        bv_name = ''
        fl = 0
        for j in range(0, le):
            if (i[j] == '['):
                bv_name = i[0:j]
                fl = 1
        if (fl == 0):
            bv_name = i
        if not BV_list.get(bv_name):
            continue
        pname = BV_list[bv_name]
        clearsecond(i, pname)

def main():
    cs()

if __name__ == '__main__':
    main()