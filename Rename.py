import os
import csv
import cv2
import shutil

def main():

    hashmap1 = {}

    with open('./url.csv', 'rt', encoding='utf-8') as f:
        cr = csv.reader(f)
        for row in cr:
            tmp1 = list(row)
            if(len(tmp1) <= 0):
                continue
            hashmap1[tmp1[2]] = tmp1[0]

    video_dirpath1 = './video'
    video_dirpathlist1 = os.listdir(video_dirpath1)
    for i in video_dirpathlist1:
        video_dirpath2 = video_dirpath1 + '/' + i # 哪个人
        video_dirpathlist2 = os.listdir(video_dirpath2)
        for j in video_dirpathlist2:
            video_dirpath3 = video_dirpath2 + '/' + j #哪个视频的文件夹
            video_dirpathlist3 = os.listdir(video_dirpath3)
            for k in video_dirpathlist3:
                le = len(k)
                if k[-3:] != 'mp4':
                    continue
                video_title = k[0: le - 3]
                if ((not video_title in hashmap1) and (not j in hashmap1)):
                    continue
                video_bv = ''
                if video_title in hashmap1:
                    video_bv = hashmap1[video_title]
                else:
                    video_bv = hashmap1[j]
                video_new_pos = './videosource/' + i
                if not os.path.exists(video_new_pos):
                    os.makedirs(video_new_pos)
                if os.path.exists(video_new_pos + '/' + video_bv + '.mp4'):
                    continue
                if os.path.exists(video_new_pos + '/' + video_bv + '.flv'):
                    continue
                video_dirpath4 = video_dirpath3 + '/' + k
                video_dirpath5 = video_new_pos + '/' + video_bv + '.mp4'
                print(video_dirpath4)
                print(video_dirpath5)
                print('\n')
                shutil.copyfile(video_dirpath4, video_dirpath5)


if __name__ == '__main__':
    main()