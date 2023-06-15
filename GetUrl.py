#!/usr/bin/python

# -*- coding: utf-8 -*-
import random
import time
from urllib import parse
from GetCover import *
from main import *
import requests
from lxml import etree
import os
import pickle
import shutil
import subprocess
from PIL import Image
import face_recognition
import numpy as np
import scipy
from keras.models import Model
from keras.layers import Input
from keras_vggface.vggface import VGGFace
from keras_vggface import utils
from PIL import Image
from init import *
from fake_useragent import UserAgent
from TestProxy import *
#from main import *



def dec(x):
    table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
    tr = {}
    for i in range(58):
        tr[table[i]] = i
    s = [11, 10, 3, 8, 4, 6]
    xor = 177451812
    add = 8728348608
    r=0
    for i in range(6):
        r+=tr[x[s[i]]]*58**i
    return (r-add)^xor

def enc(x):
    table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
    tr = {}
    for i in range(58):
        tr[table[i]] = i
    s = [11, 10, 3, 8, 4, 6]
    xor = 177451812
    add = 8728348608
    x=(x^xor)+add
    r=list('BV1  4 1 7  ')
    for i in range(6):
        r[s[i]]=table[x//58**i%58]
    return ''.join(r)


def geturl(keyword, hashmap1, hashmap2, key, list2, ff):

    urlword = parse.quote(keyword)
    if urlword in hashmap2:
        return urlword
    url = "https://search.bilibili.com/all?keyword=" + urlword
    headers = {'User-Agent': UserAgent().random}
    # lenn = len(list2)
    # pp = random.randint(0, lenn - 1)
    # while(test_proxy(list2[pp]) <= 0):
    #     pp = random.randint(0, lenn - 1)
    proxy = '115.218.0.28:9000' # list2[pp]
    proxies = {
        'http': 'http://{}'.format(proxy),
        'https': 'https://{}'.format(proxy),
    }
    #url = "https://search.bilibili.com/all?keyword=%E5%93%88%E5%85%8B"
    # headers = {
    #             'accept' : '* / *',
    #             'accept-encoding' : 'gzip, deflate, br',
    #             'accept-language' : 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
    #             'content-length' : '0',
    #             'content-type' : 'text/plain;charset=UTF-8',
    #             'cookie' : "buvid3=0AD03E74-2FCF-4F9C-B39B-8391B779B14370406infoc; rpdid=|(k|~kRkuk)u0J'ulmR)|lYkR; LIVE_BUVID=AUTO4815948166505086; buvid_fp=0AD03E74-2FCF-4F9C-B39B-8391B779B14370406infoc; _uuid=E8CAC8F8-E073-1FE2-F9F2-BD7305507C9583719infoc; sid=a9emirl7; fingerprint=6b7ad0a7a98104cc643b7ead16aee5a4; buvid_fp_plain=46AADC50-AB2F-4BA1-9AE7-672E712083BC167635infoc; CURRENT_QUALITY=116; video_page_version=v_old_home; b_ut=5; i-wanna-go-back=2; bp_video_offset_71155034=604924801957848221; bp_t_offset_71155034=604978020893482942; CURRENT_BLACKGAP=0; blackside_state=0; go_old_video=1; innersign=1; CURRENT_FNVAL=2000; bsource=search_bing; b_lsid=FB1075E4D_17E4E8D38F3; PVID=4",
    #             'origin' : 'https://search.bilibili.com',
    #             'sec-fetch-dest' : 'empty',
    #             'sec-fetch-mode' : 'no-cors',
    #             'sec-fetch-site' : 'same-site',
    #             'user-agent' : 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 97.0.4692.71 Safari / 537.36'
    #             }

    l = ""
    cnt = 0
    #list3 = []
    for i in range(1, 3 + ff):
        pos = str(i)
        if(i == 1):
            url1 = url
        else:
            url1 = url + "&page=" + pos
        response = requests.get(url1, headers = headers, timeout=10)
        #print(response)
        resp_txt = response.text
        #print(resp_txt)
        resp_html = etree.HTML(resp_txt) #//*[@id="all-list"]/div[1]/ul/li[1]
        if(i == 1):
            video_list = resp_html.xpath('//*[@id="all-list"]/div[1]/div[2]/ul[@class="video-list clearfix"]/li[@class="video-item matrix"]')
        else:
            video_list = resp_html.xpath('//*[@id="all-list"]/div[1]/ul[@class="video-list clearfix"]/li[@class="video-item matrix"]')
        for j in video_list:
            cnt += 1
            print(keyword + " " + str(cnt) + "\n")
            video_url = j.xpath('./div/div[@class="headline clearfix"]/a/@href')[0][2:]
            video_bv = j.xpath('./div/div[@class="headline clearfix"]/a/@href')[0][25:37]
            video_title = j.xpath('./div/div[@class="headline clearfix"]/a/@title')[0]

            video_title = video_title.replace(",", " ")
            if(video_bv[0:2] == 'av'):
                tmpav = ''
                for i in range(2, len(video_bv)):
                    if(video_bv[i] >= '0' and video_bv[i] <= '9'):
                        tmpav += video_bv[i]
                video_bv = enc(int(tmpav))
            if video_bv in hashmap1:
                continue
            #video_cover = Image.open(video_cover_name)
            try:
                # time.sleep(4)
                video_cover_name = getcover(video_bv)
                video_cover = face_recognition.load_image_file(video_cover_name, mode = 'RGB')
                face_boxes = face_recognition.face_locations(np.array(video_cover))
                len1 = len(face_boxes)
                os.remove(video_cover_name)
                if (len1 != 1):
                    continue
                l += video_bv + ',' + video_url + ',' + video_title + ',' + urlword + ',' + key + '\n'
                #list3.append(video_bv)
            except Exception as e:
                print(e)
                continue

    #hashmap2[urlword] = 1



    with open('./url.csv', 'a', encoding='utf-8') as f:
        f.writelines(l)

    with open('./keywords.csv', 'a', encoding='utf-8') as f:
        f.writelines(urlword + '\n')

    return urlword
