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
    for i in frame_list:
        l = ''
        point_name = frame_dir + '/' + i + '/point.txt'
        if not os.path.exists(point_name):
            continue
        gap_name = frame_dir + '/' + i + '/gap.txt'
        if not os.path.exists(gap_name):
            continue
        file_list = os.listdir(frame_dir + '/' + i)
        le = len(file_list)
        flag = []
        for j in range(0, le):
            flag.append(0)
        with open(point_name, 'rt', encoding='utf-8') as f:
            for line in f:
                tmp1 = line.split( )
                flag[int(tmp1[0])] = 1
        ffll = 0
        for j in range(1, le - 3):
            if(flag[j] == 1 and ffll == 0):
                ffll = 1
                l += str(j) + ' '
            elif(flag[j] == 0 and ffll == 1):
                ffll = 0
                l += str(j - 1) + '\n'
        if(ffll == 1):
            l += str(le - 4) + '\n'
        with open(gap_name, 'w', encoding='utf-8') as f:
            f.writelines(l)

if __name__ == '__main__':
    main()