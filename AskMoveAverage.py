import os
import multiprocessing
import os.path
import time
import face_recognition
import numpy as np
import subprocess
from PIL import Image

class frm:
    def __init__(self, pos, h1, l1, h2, l2):
        self.pos = pos
        self.h1 = h1
        self.l1 = l1
        self.h2 = h2
        self.l2 = l2

def main():
    frame_dir = './frame'
    frame_list = os.listdir(frame_dir)
    cnt = 0
    sum = 0.0
    sum1 = 0.0
    sum2 = 0.0
    l = ''
    frame_change_list = []
    for i in frame_list:
        point_name = frame_dir + '/' + i + '/point.txt'
        if not os.path.exists(point_name):
            continue
        if not os.path.exists(frame_dir + '/' + i + '/00001.jpg'):
            continue
        frame = Image.open(frame_dir + '/' + i + '/00001.jpg')
        width = frame.size[0]  # 宽
        height = frame.size[1]  # 高
        # print(i + ' ' + str(width) + ' ' + str(height))
        ter = []
        with open(point_name, 'rt', encoding='utf-8') as f:
            for line in f:
                tmp1 = line.split( )
                tmp2 = frm(int(tmp1[0]), int(tmp1[1]), int(tmp1[2]), int(tmp1[3]), int(tmp1[4]))
                ter.append(tmp2)
        le = len(ter)
        ll = ''
        for j in range(1, le):
            if(ter[j].pos != ter[j - 1].pos + 1):
                continue
            cnt += 1
            px0 = (ter[j - 1].h1 + ter[j - 1].h2) / 2
            py0 = (ter[j - 1].l1 + ter[j - 1].l2) / 2
            px1 = (ter[j].h1 + ter[j].h2) / 2
            py1 = (ter[j].l1 + ter[j].l2) / 2
            tx = px1 - px0
            ty = py1 - py0
            bilix = tx / height
            biliy = ty / width
            sum1 += abs(bilix)
            sum2 += abs(biliy)
            lam = (bilix * bilix + biliy * biliy)**0.5
            l += i + ' ' + str(ter[j].pos) + ' ' + str(bilix) + ' ' + str(biliy) + ' ' + str(lam) + '\n'
            ll += i + ' ' + str(ter[j].pos) + ' ' + str(bilix) + ' ' + str(biliy) + ' ' + str(lam) + '\n'

        with open(frame_dir + '/' + i + '/move.txt', 'w', encoding='utf-8') as f:
            f.writelines(ll)

    la = (sum1 * sum1 + sum2 * sum2)**0.5 / cnt
    with open('./MoveAverage.txt', 'w', encoding='utf-8') as f:
        f.write(str(sum1) + ' ' + str(sum2) + ' ' + str(cnt) + ' ' + str(sum1 / cnt) + ' ' + str(sum2 / cnt) + ' ' + str(la))
    # le = len(frame_change_list)
    # for i in range(0, le):
    #     l += str(frame_change_list[i]) + '\n'
    with open('./face_move.txt', 'w', encoding='utf-8') as f:
        f.writelines(l)

if __name__ == '__main__':
    main()