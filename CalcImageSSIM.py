import os

import keras
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

def ask():
    l = ''

    with open('./LargeMove.txt', 'rt', encoding='utf-8') as f:
        for line in f:
            tmp1 = line.split()
            bv_name = tmp1[0]
            bv_dir = './frame/' + bv_name + '/'
            exception_frame = bv_dir + get_num(int(tmp1[1])) + '.jpg'
            exception_before_frame = bv_dir + get_num(int(tmp1[1]) - 1) + '.jpg'
            if(not os.path.exists(exception_frame)):
                continue
            print(bv_dir)
            l += tmp1[0] + ' ' + tmp1[1] + ' ' + tmp1[4] + ' ' + str(Ssim(exception_frame, exception_before_frame)) + '\n'

    with open('./ssim1.txt', 'w', encoding='utf-8') as f:
        f.writelines(l)

def ask1():
    l = ''

    with open('./MiddleMove.txt', 'rt', encoding='utf-8') as f:
        for line in f:
            tmp1 = line.split()
            bv_name = tmp1[0]
            bv_dir = './frame/' + bv_name + '/'
            exception_frame = bv_dir + get_num(int(tmp1[1])) + '.jpg'
            exception_before_frame = bv_dir + get_num(int(tmp1[1]) - 1) + '.jpg'
            if(not os.path.exists(exception_frame)):
                continue
            l += tmp1[0] + ' ' + tmp1[1] + ' ' + tmp1[4] + ' ' + str(Ssim(exception_frame, exception_before_frame)) + '\n'

    with open('./ssim2.txt', 'w', encoding='utf-8') as f:
        f.writelines(l)

def ask2(num):
    l = ''
    ccc = -1
    with open('./MiddleMove.txt', 'rt', encoding='utf-8') as f:
        for line in f:
            tmp1 = line.split()
            bv_name = tmp1[0]
            bv_dir = './frame/' + bv_name + '/'
            exception_frame = bv_dir + get_num(int(tmp1[1])) + '.jpg'
            exception_before_frame = bv_dir + get_num(int(tmp1[1]) - 1) + '.jpg'
            if (not os.path.exists(exception_frame)):
                continue
            ccc += 1
            if(ccc % 8 != num):
                continue
            l += tmp1[0] + ' ' + tmp1[1] + ' ' + tmp1[4] + ' ' + str(
                Ssim(exception_frame, exception_before_frame)) + '\n'

    with open('./ssim2.txt', 'w', encoding='utf-8') as f:
        f.writelines(l)

def main():
    ask()
    # print(Ssim('./frame/BV1aA411u7Kt/00001.jpg', './frame/BV1aA411u7Kt/00002.jpg'))

if __name__ == '__main__':
    main()

# print('mse value:',mse)




