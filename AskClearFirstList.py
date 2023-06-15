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

def clearfirst(destination_dir, video_bv, personal_face_encoding):

    frame_dir = './frame/' + video_bv
    fl = 0
    if not os.path.exists(frame_dir):
        os.makedirs(frame_dir)
    # extract_frames = "ffmpeg -nostats -loglevel 0 -i {0}{1}.mp4 {2}/%02d.jpg".format(destination_dir,
    #                                                                                  video_bv,
    #                                                                                  frame_dir)
    data_suffix = ''
    if(os.path.exists(destination_dir + video_bv + '.mp4')):
        data_suffix = '.mp4'
    elif(os.path.exists(destination_dir + video_bv + '.flv')):
        data_suffix = '.flv'
    else:
        return
    extract_frames = 'ffmpeg -i ' + destination_dir + video_bv + data_suffix + ' -f image2 -vf fps=fps=1 -qscale:v 2 ' + frame_dir + '/%05d.jpg'
    # extract_frames = 'ffmpeg -i ' + destination_dir + video_bv + '.mp4 -vf "select=(gte(t\,1))*(isnan(prev_selected_t)+gte(t-prev_selected_t\,1))" -vsync 0 ' + frame_dir + '/%05d.jpeg'
    print(extract_frames)
    # ffmpeg -i /data/video_1.mp4 -f image2 -vf fps=fps=1/60 -qscale:v 2 /data/mp4-%05d.jpeg,
    # ffmpeg -i test.mp4 -vf "select=(gte(t\,0.5))*(isnan(prev_selected_t)+gte(t-prev_selected_t\,0.5))" -vsync 0 aaaaaaa_%05d.jpg
    # -stats (global) Print encoding progress/statistics. It is on by default, to explicitly disable it you need to specify -nostats.
    # -loglevel [flags+]loglevel | -v [flags+]loglevel
    # Set logging level and flags used by the library.
    frame_list = os.listdir(frame_dir)
    if(not os.path.exists(frame_dir + '/FinishFfmpeg.txt')):
        rs = subprocess.Popen(extract_frames, stdout=FNULL, shell=True).communicate()
    with open(frame_dir + '/FinishFfmpeg.txt', 'w', encoding='utf-8') as f:
        f.write('cnmd!')
    fl1 = 0
    # while(fl1 == 0):
    #     if (rs.poll()):
    #         fl1 = 1
    #         break
    #     else:
    #         time.sleep(1)
    frame_list = os.listdir(frame_dir)
    frame_cnt = len(frame_list)
    l = 0
    fl2 = 0
    tex1 = ''
    tex2 = ''
    now_cnt = 0
    if ((not os.path.exists(frame_dir + '/gap.txt')) and (not os.path.exists(frame_dir + '/point.txt'))):
        for i in frame_list:
            if(i[-3:] != 'jpg'):
                continue
            now_cnt += 1
            frame = Image.open(frame_dir + '/' + get_num(now_cnt) + '.jpg')
            face_boxes = face_recognition.face_locations(np.array(frame))
            # face_boxes = face_recognition.face_locations(np.array(frame), model='cnn')
            if(len(face_boxes) == 1):
                # 还得判断这张脸是不是我们要的人
                unknown_face_encoding = face_recognition.face_encodings(np.array(frame))[0]
                result = face_recognition.compare_faces([unknown_face_encoding], personal_face_encoding, 0.50)
                if(result[0] == True):
                    if (fl2 == 0):
                        fl2 = 1
                        l = now_cnt
                    tex2 += str(now_cnt) + ' ' + str(face_boxes[0][0]) + ' ' + str(face_boxes[0][1]) + ' ' + str(face_boxes[0][2]) + ' ' + str(face_boxes[0][3]) + '\n'
                    print(now_cnt)
                else:
                    if (fl2 == 1):
                        if (l >= 1):
                            tex1 += str(l) + ' ' + str(now_cnt - 1) + '\n'
                        fl2 = 0

            else:
                if(fl2 == 1):
                    if(l >= 1):
                        tex1 += str(l) + ' ' + str(now_cnt - 1) + '\n'
                    fl2 = 0

        if(fl2 == 1):
            tex1 += str(l) + ' ' + str(now_cnt) + '\n'
        with open(frame_dir + '/gap.txt', 'w', encoding='utf-8') as f:
            f.write(tex1)
        with open(frame_dir + '/point.txt', 'w', encoding='utf-8') as f:
            f.write(tex2)
        # 视频长度预订10s

def asklist():
    cnt = 0
    cnt1 = 0
    l = ''
    person_name = os.listdir('./videosource')
    for j in person_name:
        # print(j)
        # personal_face_encoding = face_recognition.face_encodings(np.array(Image.open('./face/' + j + '.jpg')))[0]
        if (not os.path.exists('./videosource/' + j)):
            continue
        video_list = os.listdir('./videosource/' + j)
        for i in video_list:
            le = len(i)
            if (i[-3:] != 'mp4' and i[-3:] != 'flv'):
                continue
            cnt1 += 1
            video_tmpbv = i[0:le - 4]
            # clearfirst('./videosource/' + person_name[0] + '/', video_tmpbv, personal_face_encoding)
            l += './videosource/' + j + '/' + ' ' + video_tmpbv + ' ' + j + '\n'
    # with open("./list.txt", "r", encoding='utf-8') as f:
    #     for line1 in f:
    #         cnt += 1
    #         if (cnt % 3 == 1):
    #             person_name = line1.split()
    #             print(person_name[0])
    #             personal_face_encoding = face_recognition.face_encodings(np.array(Image.open('./face/' + person_name[0] + '.jpg')))[0]
    #             if (not os.path.exists('./videosource/' + person_name[0])):
    #                 continue
    #             video_list = os.listdir('./videosource/' + person_name[0])
    #             for i in video_list:
    #                 le = len(i)
    #                 if (i[-3:] != 'mp4' and i[-3:] != 'flv'):
    #                     continue
    #                 cnt1 += 1
    #                 video_tmpbv = i[0:le - 4]
    #                 # clearfirst('./videosource/' + person_name[0] + '/', video_tmpbv, personal_face_encoding)
    #                 l += './videosource/' + person_name[0] + '/' + ' ' + video_tmpbv + ' ' + person_name[0] + '\n'
    #                 #if (cnt1 >= 3):
    #                 #    break
    #
    #         # if (cnt1 == 3):
    #         #    break
    with open('./ClearFirstList.txt', 'w', encoding='utf-8') as f:
        f.write(l)

def ctct(num):
    cnt = -1
    print(num)
    with open('./ClearFirstList.txt', 'rt', encoding='utf-8') as f:
        for line1 in f:
            cnt += 1
            if(cnt % 8 != num):
                continue
            # print(cnt)
            video_information = line1.split()
            print(video_information[2])
            tmp1 = Image.open('./face/' + video_information[2] + '.jpg')
            tmp2 = np.array(tmp1)
            personal_face_encoding = face_recognition.face_encodings(tmp2)[0]
            clearfirst(video_information[0], video_information[1], personal_face_encoding)


def main():

    asklist()
    # cc(1)
    # personal_face_encoding = face_recognition.face_encodings(np.array(Image.open('./face/' + '朗朗' + '.jpg')))[0]
    # clearfirst('./videosource/朗朗/', 'BV1aA411u7Kt', personal_face_encoding)

if __name__ == '__main__':
    main()