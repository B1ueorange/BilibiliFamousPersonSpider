#!/usr/bin/python

# -*- coding: utf-8 -*-

import _thread
import multiprocessing
import os.path
import time
import face_recognition
import numpy as np
import subprocess
from PIL import Image

FNULL = open(os.devnull, 'w')

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

def calc(num):
    
    cnt = -1
    
    second_frame_list = os.listdir('./frameSecond')
    for i in second_frame_list:
        second_person_frame_list = os.listdir('./frameSecond/' + i)
        personal_face_encoding = face_recognition.face_encodings(np.array(Image.open('./face/' + i + '.jpg')))[0]
        if not os.path.exists('./frameThird_1/' + i):
            os.makedirs('./frameThird_1/' + i)
        for j in second_person_frame_list:
            cnt += 1
            if(cnt % 8 != num):
                continue
            if(not os.path.exists('./frame/' + j)):
                continue
            if(not os.path.exists('./frameSecond/' + i + '/' + j + '/gap.txt')):
                continue
            frame_list = os.listdir('./frame/' + j)
            if(os.path.exists('./frameThird_1/' + i + '/' + j + '/gap.txt')):
                continue
            if not os.path.exists('./frameThird_1/' + i + '/' + j):
                os.makedirs('./frameThird_1/' + i + '/' + j)
            le = len(frame_list)
            flag1 = []
            for k in range(0, le):
                flag1.append(0)
            fl1 = 0
            s = ''
            l = 0
            with open('./frameSecond/' + i + '/' + j + '/gap.txt', 'rt', encoding = 'utf-8') as f:
                for line in f:
                    tmp1 = line.split( )
                    ll = int(tmp1[0])
                    rr = int(tmp1[1])
                    for k in range(ll, rr + 1):
                        if not os.path.exists('./frame/' + j + '/' + get_num(k) + '.jpg'):
                            continue
                        frame = Image.open('./frame/' + j + '/' + get_num(k) + '.jpg')
                        print(j + ' ' + str(cnt) + ' ' + str(k))
                        unknown_face_encoding = face_recognition.face_encodings(np.array(frame))[0]
                        result = face_recognition.compare_faces([unknown_face_encoding], personal_face_encoding, 0.50)
                        if(result[0] == True):
                            flag1[k] = 1
                        if(flag1[k] == 1):
                            if(fl1 == 0):
                                fl1 = 1
                                l = k
                        else:
                            if(fl1 == 1):
                                fl1 = 0
                                s += str(l) + ' ' + str(k - 1) + '\n'
                    if (fl1 == 1):
                        s += str(l) + ' ' + str(rr) + '\n'
                        fl1 = 0
            with open('./frameThird_1/' + i + '/' + j + '/gap.txt', 'w', encoding = 'utf-8') as f:
                f.writelines(s)



def main():

    try:
        p0 = multiprocessing.Process(target=calc, args=(0, ))
        p1 = multiprocessing.Process(target=calc, args=(1, ))
        p2 = multiprocessing.Process(target=calc, args=(2, ))
        p3 = multiprocessing.Process(target=calc, args=(3, ))
        p4 = multiprocessing.Process(target=calc, args=(4, ))
        p5 = multiprocessing.Process(target=calc, args=(5, ))
        p6 = multiprocessing.Process(target=calc, args=(6, ))
        p7 = multiprocessing.Process(target=calc, args=(7, ))


        p0.start()
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()
        p6.start()
        p7.start()

        p0.join()
        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()
        p6.join()
        p7.join()

        

    except Exception as e:
        print(e)



if __name__ == '__main__':
    main()