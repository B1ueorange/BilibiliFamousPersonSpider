import multiprocessing
import os.path
import time
import face_recognition
import numpy as np
import subprocess
from PIL import Image

def main():
    frame_dir = './frame'
    frame_list = os.listdir(frame_dir)
    l = ''
    for i in frame_list:
        point_name = frame_dir + '/' + i + '/point.txt'
        if not os.path.exists(point_name):
            continue
        gap_name = frame_dir + '/' + i + '/gap.txt'
        if not os.path.exists(gap_name):
            continue
        file_list = os.listdir(frame_dir + '/' + i)
        le = len(file_list)
        flag = []
        flag2 = []
        for j in range(0, le):
            flag.append(0)
            flag2.append(0)
        with open(point_name, 'rt', encoding='utf-8') as f:
            for line in f:
                tmp1 = line.split( )
                flag[int(tmp1[0])] = 1
        with open(gap_name, 'rt', encoding='utf-8') as f:
            for line in f:
                flag1 = 0
                tmp1 = line.split()
                ll = int(tmp1[0])
                rr = int(tmp1[1])
                for j in range(ll, rr + 1):
                    flag2[j] = 1
                    if(flag[j] != 1):
                        if(flag1 == 0):
                            flag1 = 1
                            l += i + '\n' + tmp1[0] + ' ' + tmp1[1] + '\n'
                        l += str(j) + ' '
                if(flag1 == 1):
                    l += '\n'
        flag1 = 0
        for j in range(1, le - 3):
            if(flag[j] == 1 and flag2[j] == 0):
                if(flag1 == 0):
                    flag1 = 1
                    l += i + '\n'
                l += str(j) + ' '
        if(flag1 == 1):
            l += '\n'

    with open('./Error.txt', 'w', encoding='utf-8') as f:
        f.writelines(l)

if __name__ == '__main__':
    main()