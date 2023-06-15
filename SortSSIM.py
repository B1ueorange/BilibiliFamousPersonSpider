import os

import keras
from PIL import Image
import pytorch_ssim
import torch
import torchvision
import torch.autograd

def ask():
    ter = []
    with open('./ssim1.txt', 'rt', encoding='utf-8') as f:
        for line in f:
            tmp1 = line.split( )
            if(float(tmp1[2]) >= 0.350000):
                continue
            ter.append((tmp1[0], tmp1[1], tmp1[2], float(tmp1[3])))
    ter.sort(key = lambda s:(s[3]))
    with open('./ssim1_sort.txt', 'w', encoding='utf-8') as f:
        l = ''
        for i in ter:
            l += i[0] + ' ' + i[1] + ' ' + i[2] + ' ' + str(i[3]) + '\n'
        f.writelines(l)

def main():
    ask()
    # print(Ssim('./frame/BV1aA411u7Kt/00001.jpg', './frame/BV1aA411u7Kt/00002.jpg'))

if __name__ == '__main__':
    main()
