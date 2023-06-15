import multiprocessing
import os.path
import time
import face_recognition
import numpy as np
import subprocess
from PIL import Image

def ask1():
    frame_dir = './frame'
    frame_list = os.listdir(frame_dir)
    l = ''
    ll = ''
    mx = 0.0
    mi = 1.0
    sum = 0.0
    cnt = 0
    ter = []
    for i in frame_list:
        if not os.path.exists(frame_dir + '/' + i + '/00001.jpg'):
            continue
        frame = Image.open(frame_dir + '/' + i + '/00001.jpg')
        width = frame.size[0]  # 宽
        height = frame.size[1]  # 高
        point_name = frame_dir + '/' + i + '/point.txt'
        if not os.path.exists(point_name):
            continue
        file_list = os.listdir(frame_dir + '/' + i)
        le = len(file_list)
        with open(point_name, 'rt', encoding='utf-8') as f:
            for line in f:
                tmp1 = line.split()
                face_area = abs(int(tmp1[3]) - int(tmp1[1])) * abs(int(tmp1[4]) - int(tmp1[2]))
                bili = face_area / (width * height)
                cnt += 1
                sum += bili
                mx = max(mx, bili)
                mi = min(mi, bili)
                ter.append((i, tmp1[0], bili))

    ter.sort(key = lambda s:(s[2]))

    l = str(mx) + ' ' + str(mi) + ' ' + str(sum / cnt) + ' ' + str(sum) + ' ' + str(cnt) + '\n'
    with open('./FaceAverage.txt', 'w', encoding='utf-8') as f:
        f.writelines(l)
    with open('./FaceArea.txt', 'w', encoding='utf-8') as f:
        for i in ter:
            ll += str(i) + '\n'
        f.writelines(ll)

def ask2():
    frame_dir = './frame'
    frame_list = os.listdir(frame_dir)
    l = ''

    mx = 0.0
    mi = 1.0
    sum = 0.0
    cnt = 0

    for i in frame_list:
        ter = []
        ll = ''
        ter.clear()
        if not os.path.exists(frame_dir + '/' + i + '/00001.jpg'):
            continue
        frame = Image.open(frame_dir + '/' + i + '/00001.jpg')
        width = frame.size[0]  # 宽
        height = frame.size[1]  # 高
        point_name = frame_dir + '/' + i + '/point.txt'
        if not os.path.exists(point_name):
            continue
        file_list = os.listdir(frame_dir + '/' + i)
        le = len(file_list)
        with open(point_name, 'rt', encoding='utf-8') as f:
            for line in f:
                tmp1 = line.split()
                face_area = abs(int(tmp1[3]) - int(tmp1[1])) * abs(int(tmp1[4]) - int(tmp1[2]))
                bili = face_area / (width * height)
                cnt += 1
                sum += bili
                mx = max(mx, bili)
                mi = min(mi, bili)
                ter.append((i, tmp1[0], bili))
        # ter.sort(key=lambda s: (s[2]))
        with open(frame_dir + '/' + i + '/area.txt', 'w', encoding='utf-8') as f:
            for i in ter:
                ll += str(i[0]) + ' ' + str(i[1]) + ' ' + str(i[2]) + '\n'
            f.writelines(ll)


def main():

    ask2()

if __name__ == '__main__':
    main()