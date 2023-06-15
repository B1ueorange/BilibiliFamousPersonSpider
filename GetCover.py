#!/usr/bin/python

# -*- coding: utf-8 -*-

import os
import json
import requests
import chardet
from fake_useragent import UserAgent

# 随机产生请求头
#ua = UserAgent(verify_ssl=False, path='D:/Pycharm/fake_useragent.json')


# 随机切换请求头
def random_ua():
    headers = {
        'accept' : '* / *',
                'accept-encoding' : 'gzip, deflate, br',
                'accept-language' : 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
                'content-length' : '0',
                'content-type' : 'text/plain;charset=UTF-8',
                'cookie' : "buvid3=0AD03E74-2FCF-4F9C-B39B-8391B779B14370406infoc; rpdid=|(k|~kRkuk)u0J'ulmR)|lYkR; LIVE_BUVID=AUTO4815948166505086; _uuid=E8CAC8F8-E073-1FE2-F9F2-BD7305507C9583719infoc; sid=a9emirl7; video_page_version=v_old_home; CURRENT_BLACKGAP=0; blackside_state=0; go_old_video=1; buvid4=D6175008-EC22-A439-EBFF-DB3701D5F94A07209-022012016-Qwha2QbSl+mlNNtl6wQnug==; buvid_fp_plain=undefined; DedeUserID=71155034; DedeUserID__ckMd5=469a8dda68b91542; SESSDATA=0f5f3c15,1658497394,ac83f*11; bili_jct=edd0ca9ad6c860111fd27664992a1f9a; b_ut=5; i-wanna-go-back=2; CURRENT_QUALITY=116; fingerprint=bb9d1cc25f26cb7c62f7367e2f773234; buvid_fp=bb9d1cc25f26cb7c62f7367e2f773234; bsource=search_bing; bp_t_offset_71155034=629544946059223255; CURRENT_FNVAL=80; b_lsid=8A5F878D_17F2BB96617; PVID=4; bp_video_offset_71155034=630782210264268819; nostalgia_conf=2; CURRENT_FNVAL=4048; innersign=0",
                'origin' : 'https://search.bilibili.com',
                'sec-fetch-dest' : 'document',
                'sec-fetch-mode' : 'no-cors',
                'sec-fetch-site' : 'none',
                'user-agent' : 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 97.0.4692.71 Safari / 537.36'

    }
    return headers


#  创建文件夹
def path_creat():
    _path = "./cover"
    if not os.path.exists(_path):
        os.mkdir(_path)
    return _path



def dec(x):
    table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
    tr = {}
    for i in range(58):
        tr[table[i]] = i
    s = [11, 10, 3, 8, 4, 6]
    xor = 177451812
    add = 8728348608
    r = 0
    for i in range(6):
        r+=tr[x[s[i]]]*58**i
    return (r-add)^xor



# 对爬取的页面内容进行json格式处理
def get_text(url):
    res = requests.get(url=url, headers=random_ua())
    res.encoding = chardet.detect(res.content)['encoding']  # 统一字符编码
    res = res.text
    data = json.loads(res)  # json格式化
    return data


# 根据bv号获取av号
def get_aid(bv):

    return dec(bv)


# 根据av号获取封面图片
def get_image(aid):
    url_3 = 'https://api.bilibili.com/x/web-interface/view?aid={}'.format(aid)
    response_3 = get_text(url_3)
    image_url = response_3['data']['pic']  # 获取图片的下载连接
    image = requests.get(url=image_url, headers=random_ua()).content  # 获取图片
    return image


# 下载封面
def download(image, file_name):
    with open(file_name, 'wb') as f:
        f.write(image)
        f.close()


def download1(BV, file_name):
    BV_number = BV
    search_url = 'https://search.bilibili.com/all?keyword=' + str(BV_number) + '&from_source=nav_search_new'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"}
    response = requests.get(search_url, headers=headers)  # 获取网页源代码
    page_text = response.text

    a = page_text.find(r'"pic":"')
    b = page_text.find(r'jpg')
    need_image = page_text[a + 7:b + 3].encode("utf-8").decode("unicode_escape")
    print(need_image)
    image_url = "https:" + str(need_image)

    with open(file_name, 'wb') as f:
        img = requests.get(image_url)
        f.write(img.content)

def getcover(BV):
    path = path_creat()
    aid = ''
    if(BV[0:2] == 'BV'):
        aid = get_aid(BV)
    else:
        for i in range(2, len(BV)):
            if(BV[i] >= '0' and BV[i] <= '9'):
                aid += BV[i]
    image = get_image(aid)
    file_name = path + '/{}.jpg'.format(BV)
    download(image, file_name)
    # download1(BV, file_name)
    return file_name

'''
def main():
    k = 'Y'
    while k == 'Y':  # 根据用户需要一直循环
        path = path_creat()  # 创建保存B站封面的文件夹
        bv = input("请输入视频的bv号：")
        image_name = input("请你给想要下载的封面取一个喜欢的名字叭：")
        aid = get_aid(bv)
        image = get_image(aid)
        file_name = path + '{}.jpg'.format(image_name)
        download(image, file_name)
        print("封面提取完毕^_^")
        k = input("按Y键继续提取，按Q退出：")
'''
