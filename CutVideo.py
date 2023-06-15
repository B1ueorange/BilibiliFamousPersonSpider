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

def get_time(x):
    min = int(x / 60)
    sec = x % 60
    return str(min) + ':' + str(sec)

def calc(num):
    cnt = -1

    second_frame_list = os.listdir('./frameForth')
    for i in second_frame_list:
        second_person_frame_list = os.listdir('./frameForth/' + i)
        personal_face_encoding = face_recognition.face_encodings(np.array(Image.open('./face/' + i + '.jpg')))[0]
        if not os.path.exists('./VideoClip/' + i):
            os.makedirs('./VideoClip/' + i)
        for j in second_person_frame_list:
            cnt += 1
            if (cnt % 8 != num):
                continue
            if (not os.path.exists('./frame/' + j)):
                continue
            if (not os.path.exists('./frameForth/' + i + '/' + j + '/gap.txt')):
                continue
            frame_list = os.listdir('./frame/' + j)
            if (os.path.exists('./VideoClip/' + i + '/' + j + '/gap.txt')):
                continue
            if not os.path.exists('./VideoClip/' + i + '/' + j):
                os.makedirs('./VideoClip/' + i + '/' + j)
            cnt2 = 0
            file_name = ''
            if(os.path.exists('./videosource/' + i + '/' + j + '.mp4')):
                file_name = './videosource/' + i + '/' + j + '.mp4'
            else:
                file_name = './videosource/' + i + '/' + j + '.flv'
            with open('./frameForth/' + i + '/' + j + '/gap.txt', 'rt', encoding='utf-8') as f:
                for line in f:
                    tmp1 = line.split()
                    ll = int(tmp1[0])
                    rr = int(tmp1[1])
                    for k in range(ll, rr + 1, 4):
                        st = k
                        et = k + 4
                        if(et > rr):
                            break
                        cnt2 += 1
                        output_name = './VideoClip/' + i + '/' + j + '/' + get_num(cnt2) + '.mp4'
                        if(os.path.exists(output_name)):
                            continue
                        extract_clip = 'ffmpeg -ss ' + get_time(st) + ' -i ' + file_name + ' -t 4 ' + output_name
                        rs = subprocess.Popen(extract_clip, stdout=FNULL, shell=True).communicate()


def main():
    try:
        p0 = multiprocessing.Process(target=calc, args=(0,))
        p1 = multiprocessing.Process(target=calc, args=(1,))
        p2 = multiprocessing.Process(target=calc, args=(2,))
        p3 = multiprocessing.Process(target=calc, args=(3,))
        p4 = multiprocessing.Process(target=calc, args=(4,))
        p5 = multiprocessing.Process(target=calc, args=(5,))
        p6 = multiprocessing.Process(target=calc, args=(6,))
        p7 = multiprocessing.Process(target=calc, args=(7,))

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