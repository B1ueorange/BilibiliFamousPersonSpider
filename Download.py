import _thread
import os
import csv
import pandas as pd
import sys
import time
from you_get import common as you_get

def download(num):
    df = pd.read_csv('./url.csv', header=None, engine='python')
    le = len(df)
    cnt = 0
    pos = 0

    filename = './pos' + str(num) + '.txt'

    with open(filename, 'rt', encoding='utf-8') as f:
        cr = csv.reader(f)
        for row in cr:
            tmp3 = list(row)
            if (len(tmp3) <= 0):
                continue
            if (tmp3[0] == 'Finish'):
                return

    for i in range(0, le):
        # cnt += 1
        # if(cnt > 3):
        #    break
        tmp2 = list(df.iloc[i])
        if (len(tmp2) <= 0):
            continue
        if (i % 8 != num):
            continue
        cnt += 1
        print(i)
        print(tmp2[2])
        video_path = "./videosource/" + tmp2[4]
        video_name = video_path + "/" + tmp2[0]
        if not os.path.exists(video_path):
            os.makedirs(video_path)
        if os.path.exists(video_name + '.flv'):
            continue
        if os.path.exists(video_name + '.mp4'):
            continue
        sys.argv = ['you-get', '-t', '3000', '-o', video_path, '-O', tmp2[0], tmp2[1]]
        # sys.argv = ['you-get', '-t', '3000', '-o', video_path, 'https://www.bilibili.com/video/BV1jV411n7qa']
        flah = 0
        while flah == 0:
            try:
                #you_get.main()
                com = 'you-get -t 3000 -o ' + video_path + ' -O ' + tmp2[0] + ' ' + tmp2[1]
                os.system(com)
                flah = 1
            except Exception as e:
                flah = 0
                continue


    if (num < 7 and cnt == 171):
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines('Finish')

    if (num == 7 and cnt == 170):
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines('Finish')


def main():

    lfah = 0
    isRun = 0
    while lfah == 0:
        if(isRun == 1):
            time.sleep(1)
            continue
        try:
            isRun = 1
            _thread.start_new_thread(download, (0, ))
            _thread.start_new_thread(download, (1, ))
            _thread.start_new_thread(download, (2, ))
            _thread.start_new_thread(download, (3, ))
            _thread.start_new_thread(download, (4, ))
            _thread.start_new_thread(download, (5, ))
            _thread.start_new_thread(download, (6, ))
            _thread.start_new_thread(download, (7, ))
            # _thread.start_new_thread(os.system('python download0.py'))
            # _thread.start_new_thread(os.system('python download1.py'))
            # _thread.start_new_thread(os.system('python download2.py'))
            # _thread.start_new_thread(os.system('python download3.py'))
            # _thread.start_new_thread(os.system('python download4.py'))
            # _thread.start_new_thread(os.system('python download5.py'))
            # _thread.start_new_thread(os.system('python download6.py'))
            # _thread.start_new_thread(os.system('python download7.py'))

        except Exception as e:
            print(e)
            isRun = 0

        ccc = 0

        for i in range(0, 8):
            filename = './pos' + str(i) + '.txt'
            with open(filename, 'rt', encoding='utf-8') as f:
                cr = csv.reader(f)
                for row in cr:
                    tmp3 = list(row)
                    if (len(tmp3) <= 0):
                        continue
                    if (tmp3[0] == 'Finish'):
                        ccc += 1

        if (ccc == 8):
            lfah = 1

        # with open('./pos0.txt', 'rt', encoding='utf-8') as f:
        #     cr = csv.reader(f)
        #     for row in cr:
        #         tmp3 = list(row)
        #         if (len(tmp3) <= 0):
        #             continue
        #         if (int(tmp3[0]) == 171):
        #            ccc += 1
        #
        # with open('./pos1.txt', 'rt', encoding='utf-8') as f:
        #     cr = csv.reader(f)
        #     for row in cr:
        #         tmp3 = list(row)
        #         if (len(tmp3) <= 0):
        #             continue
        #         if (int(tmp3[0]) == 171):
        #            ccc += 1
        #
        # with open('./pos2.txt', 'rt', encoding='utf-8') as f:
        #     cr = csv.reader(f)
        #     for row in cr:
        #         tmp3 = list(row)
        #         if (len(tmp3) <= 0):
        #             continue
        #         if (int(tmp3[0]) == 171):
        #            ccc += 1
        #
        # with open('./pos3.txt', 'rt', encoding='utf-8') as f:
        #     cr = csv.reader(f)
        #     for row in cr:
        #         tmp3 = list(row)
        #         if (len(tmp3) <= 0):
        #             continue
        #         if (int(tmp3[0]) == 171):
        #            ccc += 1
        #
        # with open('./pos4.txt', 'rt', encoding='utf-8') as f:
        #     cr = csv.reader(f)
        #     for row in cr:
        #         tmp3 = list(row)
        #         if (len(tmp3) <= 0):
        #             continue
        #         if (int(tmp3[0]) == 171):
        #            ccc += 1
        #
        # with open('./pos5.txt', 'rt', encoding='utf-8') as f:
        #     cr = csv.reader(f)
        #     for row in cr:
        #         tmp3 = list(row)
        #         if (len(tmp3) <= 0):
        #             continue
        #         if (int(tmp3[0]) == 171):
        #            ccc += 1
        #
        # with open('./pos6.txt', 'rt', encoding='utf-8') as f:
        #     cr = csv.reader(f)
        #     for row in cr:
        #         tmp3 = list(row)
        #         if (len(tmp3) <= 0):
        #             continue
        #         if (int(tmp3[0]) == 171):
        #            ccc += 1
        #
        # with open('./pos7.txt', 'rt', encoding='utf-8') as f:
        #     cr = csv.reader(f)
        #     for row in cr:
        #         tmp3 = list(row)
        #         if (len(tmp3) <= 0):
        #             continue
        #         if (int(tmp3[0]) == 170):
        #            ccc += 1
        #
        # if (ccc == 8):
        #     lfah = 1


if __name__ == '__main__':
    main()