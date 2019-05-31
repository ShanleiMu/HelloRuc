# -*- coding: utf-8 -*-
# @Time    : 2019/5/23 21:21
# @Author  : Shanlei Mu
# @Email   : msl@ruc.edu.cn
# @File    : RucSpider.py

import requests
from lxml import etree
import re


# type 1
class JiWeiBanGongShi:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        self.base_url_list = ['http://jwjcc.ruc.edu.cn/gzdt/ttxw/',
                              'http://jwjcc.ruc.edu.cn/gzdt/tpxw/',
                              'http://jwjcc.ruc.edu.cn/gzdt/bx/',
                              'http://jwjcc.ruc.edu.cn/gzdt/xw/',
                              'http://jwjcc.ruc.edu.cn/tzgg/',
                              'http://jwjcc.ruc.edu.cn/fgzd/xxgz/',
                              'http://jwjcc.ruc.edu.cn/lzjy/qlwh/',
                              'http://jwjcc.ruc.edu.cn/lzjy/lzhd/',
                              ]
        self.url_list = []

    def get_url_list(self):
        for base_url in self.base_url_list:
            index = 1
            response = requests.get(base_url + 'index.htm', self.headers, verify=False)
            selector = etree.HTML(response.text)
            href_list = selector.xpath('//ul[@class="news_list"]/li/a/@href | //ul[@class="picnews_list"]/li/a/@href |'
                                       '//ul[@class="notice_list"]/li/a/@href')
            while True:
                pre_href_list = href_list
                for href in pre_href_list:
                    if 'http://' in href:
                        self.url_list.append(href)
                    else:
                        self.url_list.append(base_url + href)

                new_url = base_url + 'index' + str(index) + '.htm'
                response = requests.get(new_url, self.headers, verify=False)
                selector = etree.HTML(response.text)
                href_list = selector.xpath('//ul[@class="news_list"]/li/a/@href | '
                                           '//ul[@class="picnews_list"]/li/a/@href |'
                                           '//ul[@class="notice_list"]/li/a/@href')
                index += 1
                if pre_href_list == href_list:
                    break
        print(len(self.url_list))

    def begin_spider(self):
        with open('output/纪委办公室.txt', 'w', encoding='utf-8') as fp:
            idx = 0
            for url in self.url_list:
                if idx % 100 == 0:
                    print(idx)
                title = ''
                time = ''
                text = ''
                try:
                    response = requests.get(url, self.headers, verify=False)
                except:
                    continue
                response.encoding = 'utf-8'
                selector = etree.HTML(response.text)
                title_list = selector.xpath('//div[@class="tit"]/h4/text() | //h2[@class="tit"]/p/text()')
                time_list = selector.xpath('//div[@class="tit"]/p/span[1]/text() | //h3[@class="daty"]/div/em[2]/text()')
                text_list = selector.xpath('//div[@class="txt"]/p/text() | //div[@class="txt"]/p/span/text() | '
                                           '//div[@class="TRS_Editor"]/p/text()')
                try:
                    for title_u in title_list:
                        title += title_u
                except:
                    pass
                try:
                    time = time_list[0].split('：')[1].replace("'", '')
                except:
                    pass
                if len(text_list) == 0:
                    continue
                for text_u in text_list:
                    text += text_u
                fp.write(str(idx) + '|||' + title + '|||' + time + '|||' + url + '|||' + text.strip() + '\n')
                idx += 1


class BaoWeiChu:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        self.base_url_list = ['http://bwb.ruc.edu.cn/bszn/',
                              'http://bwb.ruc.edu.cn/tzgg/',
                              'http://bwb.ruc.edu.cn/gzdt/',
                              'http://bwb.ruc.edu.cn/xzzq/',
                              'http://bwb.ruc.edu.cn/gzzd/',
                              'http://bwb.ruc.edu.cn/aqjy/aqcs/'
                              ]
        self.url_list = []

    def get_url_list(self):
        for base_url in self.base_url_list:
            index = 1
            response = requests.get(base_url + 'index.htm', self.headers, verify=False)
            selector = etree.HTML(response.text)
            href_list = selector.xpath('//div[@class="soogee_list"]/ul/li/a/@href | '
                                       '//div[@class="work_list"]/ul/li/a/@href')
            while True:
                pre_href_list = href_list
                for href in pre_href_list:
                    if 'http://' in href or 'https://' in href:
                        self.url_list.append(href)
                    else:
                        self.url_list.append(base_url + href)

                new_url = base_url + 'index' + str(index) + '.htm'
                response = requests.get(new_url, self.headers, verify=False)
                selector = etree.HTML(response.text)
                href_list = selector.xpath('//div[@class="soogee_list"]/ul/li/a/@href | '
                                           '//div[@class="work_list"]/ul/li/a/@href')
                index += 1
                if pre_href_list == href_list:
                    break
        print(len(self.url_list))

    def begin_spider(self):
        with open('output/保卫部.txt', 'w', encoding='utf-8') as fp:
            idx = 0
            for url in self.url_list:
                # print('testtesttesttest')
                if idx % 100 == 0:
                    print(idx)
                title = ''
                time = ''
                text = ''
                try:
                    response = requests.get(url, self.headers, verify=False)
                except:
                    continue
                response.encoding = 'utf-8'
                selector = etree.HTML(response.text)
                title_list = selector.xpath('//div[@class="tit"]/h3/text()')
                time_list = selector.xpath('//div[@class="tit"]/p[@class="info"]/span[1]/text()')
                text_list = selector.xpath('//div[@class="txt"]/div/p/text() | '
                                           '//div[@class="txt"]/p/text() | '
                                           '//div[@class="txt"]/p/span/text() |'
                                           '//div[@class="txt"]/div/p/span/text()')
                try:
                    for title_u in title_list:
                        title += title_u
                except:
                    pass
                try:
                    time = time_list[0].split('：')[1].replace("'", '')
                except:
                    pass
                if len(text_list) == 0:
                    print(url)
                    continue
                for text_u in text_list:
                    text += text_u.strip()
                fp.write(str(idx) + '|||' + title + '|||' + time + '|||' + url + '|||' + text.strip() + '\n')
                idx += 1


class JiGuanDangWei:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        self.base_url_list = ['http://jgdw.ruc.edu.cn/xw2018/',
                              'http://jgdw.ruc.edu.cn/tzgg/',
                              'http://jgdw.ruc.edu.cn/djhd/',
                              'http://jgdw.ruc.edu.cn/zbfc/',
                              'http://jgdw.ruc.edu.cn/gzzd/'
                              ]
        self.url_list = []

    def get_url_list(self):
        for base_url in self.base_url_list:
            index = 1
            response = requests.get(base_url + 'index.htm', self.headers, verify=False)
            selector = etree.HTML(response.text)
            href_list = selector.xpath('//ul[@class="listimg-ul"]/li/div/h2/a/@href')
            while True:
                pre_href_list = href_list
                for href in pre_href_list:
                    if 'http://' in href or 'https://' in href:
                        self.url_list.append(href)
                    else:
                        self.url_list.append(base_url + href)

                new_url = base_url + 'index' + str(index) + '.htm'
                response = requests.get(new_url, self.headers, verify=False)
                selector = etree.HTML(response.text)
                href_list = selector.xpath('//ul[@class="listimg-ul"]/li/div/h2/a/@href |'
                                           '//ul[@class="listnoimg-ul"]/li/div/h2/a/@href')
                index += 1
                if pre_href_list == href_list:
                    break
        print(len(self.url_list))

    def begin_spider(self):
        with open('output/机关党委.txt', 'w', encoding='utf-8') as fp:
            idx = 0
            for url in self.url_list:
                if idx % 100 == 0:
                    print(idx)
                title = ''
                time = ''
                text = ''
                try:
                    response = requests.get(url, self.headers, verify=False)
                except:
                    continue
                response.encoding = 'utf-8'
                selector = etree.HTML(response.text)
                title_list = selector.xpath('//div[@class="list-info"]/h1/text()')
                time_list = selector.xpath('//div[@class="list-info"]/div[@class="aside clearfix"]/span/text()')
                text_list = selector.xpath('//div[@class="textcnt"]/p/text()')
                try:
                    for title_u in title_list:
                        title += title_u
                except:
                    pass
                try:
                    time_str = time_list[0]
                    time = re.findall(r"\d+-\d+-\d+", time_str)[0]
                except:
                    pass
                if len(text_list) == 0:
                    print(url)
                    continue
                for text_u in text_list:
                    text += text_u.strip()
                # print(url, title, time, text)
                # break
                fp.write(str(idx) + '|||' + title + '|||' + time + '|||' + url + '|||' + text.strip() + '\n')
                idx += 1


class XiaoTuanWei:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        self.base_url_list = ['http://youth.ruc.edu.cn/xwsd/',
                              'http://youth.ruc.edu.cn/ggl/'
                              ]
        self.url_list = []

    def get_url_list(self):
        for base_url in self.base_url_list:
            index = 1
            response = requests.get(base_url + 'index.htm', self.headers, verify=False)
            selector = etree.HTML(response.text)
            href_list = selector.xpath('//ul[@class="pic_list"]/li/a/@href | '
                                       '//ul[@class="normal_list"]/li/a/@href')
            while True:
                pre_href_list = href_list
                for href in pre_href_list:
                    if 'http://' in href or 'https://' in href:
                        self.url_list.append(href)
                    else:
                        self.url_list.append(base_url + href)

                new_url = base_url + 'index' + str(index) + '.htm'
                response = requests.get(new_url, self.headers, verify=False)
                selector = etree.HTML(response.text)
                href_list = selector.xpath('//ul[@class="pic_list"]/li/a/@href | '
                                           '//ul[@class="normal_list"]/li/a/@href')
                index += 1
                if pre_href_list == href_list:
                    break
        print(len(self.url_list))

    def begin_spider(self):
        with open('output/校团委.txt', 'w', encoding='utf-8') as fp:
            idx = 0
            for url in self.url_list:
                if idx % 100 == 0:
                    print(idx)
                title = ''
                time = ''
                text = ''
                try:
                    response = requests.get(url, self.headers, verify=False)
                except:
                    continue
                response.encoding = 'utf-8'
                selector = etree.HTML(response.text)
                title_list = selector.xpath('//div[@class="tit"]/h4/text()')
                time_list = selector.xpath('//div[@class="tit"]/span[1]/text()')
                text_list = selector.xpath('//div[@class="txt"]/p/text() |'
                                           '//div[@class="txt"]/p/span/text() |'
                                           '//div[@class="txt"]/div/p/span/text()')
                try:
                    for title_u in title_list:
                        title += title_u
                except:
                    pass
                try:
                    time_str = time_list[0]
                    time = re.findall(r"\d+-\d+-\d+", time_str)[0]
                except:
                    pass
                if len(text_list) == 0:
                    print(url)
                    continue
                for text_u in text_list:
                    text += text_u.strip()
                if not text:
                    print(url)
                    continue
                fp.write(str(idx) + '|||' + title + '|||' + time + '|||' + url + '|||' + text.strip() + '\n')
                idx += 1


class JiaoWuChu:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        self.base_url_list = ['http://jiaowu.ruc.edu.cn/tzgg6/',
                              'http://jiaowu.ruc.edu.cn/gjjl/',
                              'http://jiaowu.ruc.edu.cn/jxdt6/'
                              ]
        self.url_list = []

    def get_url_list(self):
        for base_url in self.base_url_list:
            index = 1
            response = requests.get(base_url + 'index.htm', self.headers, verify=False)
            selector = etree.HTML(response.text)
            href_list = selector.xpath('//ul[@class="iise"]/li/a/@href')
            while True:
                pre_href_list = href_list
                for href in pre_href_list:
                    if 'http://' in href or 'https://' in href:
                        self.url_list.append(href)
                    else:
                        self.url_list.append(base_url + href)

                new_url = base_url + 'index' + str(index) + '.htm'
                response = requests.get(new_url, self.headers, verify=False)
                selector = etree.HTML(response.text)
                href_list = selector.xpath('//ul[@class="iise"]/li/a/@href')
                index += 1
                if pre_href_list == href_list:
                    break
        print(len(self.url_list))

    def begin_spider(self):
        with open('output/教务处.txt', 'w', encoding='utf-8') as fp:
            idx = 0
            for url in self.url_list:
                if idx % 100 == 0:
                    print(idx)
                title = ''
                time = ''
                text = ''
                try:
                    response = requests.get(url, self.headers, verify=False)
                except:
                    continue
                response.encoding = 'utf-8'
                selector = etree.HTML(response.text)
                title_list = selector.xpath('//body/div[4]/div[2]/div[2]/div[1]/text()')
                time_list = selector.xpath('//body/div[4]/div[2]/div[2]/div[2]/text()')
                try:
                    text_selector = selector.xpath('//div[@class="dddeii"]')[0]
                except:
                    continue
                text_list = text_selector.xpath("string(.)")
                # text_list = selector.xpath('//div[@class="dddeii"]/p/span/text() |'
                #                            '//div[@class="dddeii"]/text() |'
                #                            '//div[@class="dddeii"]/*/text() |'
                #                            '//div[@class="dddeii"]/*/*/text() |'
                #                            '//div[@class="dddeii"]/*/*/*/text()')
                try:
                    for title_u in title_list:
                        title += title_u
                except:
                    pass
                try:
                    time_str = time_list[0]
                    time = re.findall(r"\d+-\d+-\d+", time_str)[0]
                except:
                    pass
                if len(text_list) == 0:
                    print(url)
                    continue
                for text_u in text_list:
                    text += text_u.strip()
                if not text:
                    print(url)
                    continue
                # print(url, title, time, text)
                fp.write(str(idx) + '|||' + title + '|||' + time + '|||' + url + '|||' + text.strip() + '\n')
                idx += 1


# type 2
class XueGongBu:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        self.base_url_list = ['http://xsc.ruc.edu.cn/index/bszn',
                              'http://xsc.ruc.edu.cn/index/tzgg',
                              'http://xsc.ruc.edu.cn/index/xwzx',
                              ]
        self.base_url = 'http://xsc.ruc.edu.cn/index'
        self.url_list = []

    def get_url_list(self):
        for base_url in self.base_url_list:
            idx = 1
            response = requests.get(base_url + '.htm', self.headers, verify=False)
            selector = etree.HTML(response.text)
            href_list = selector.xpath('//div[@class="m-list3"]/ul/li/div/h3/a/@href |'
                                       '//div[@class="Newslist"]/ul/li/a/@href')
            p_no_list = selector.xpath('//span[@class="p_no"][last()]/a/text()')

            if len(p_no_list) == 0:
                p_no = 1
                for href in href_list:
                    if 'http://' in href:
                        self.url_list.append(href)
                    else:
                        self.url_list.append(self.base_url + '/' + href)
            else:
                p_no = int(p_no_list[0])

            while idx < p_no:
                pre_href_list = href_list
                for href in pre_href_list:
                    if 'http://' in href:
                        self.url_list.append(href)
                    else:
                        if idx == 1:
                            self.url_list.append(self.base_url + '/' + href)
                        else:
                            self.url_list.append(base_url + '/' + href)
                new_url = base_url + '/' + str(idx) + '.htm'
                response = requests.get(new_url, self.headers, verify=False)
                selector = etree.HTML(response.text)
                href_list = selector.xpath('//div[@class="m-list3"]/ul/li/div/h3/a/@href |'
                                           '//div[@class="Newslist"]/ul/li/a/@href')
                idx += 1
        print(len(self.url_list))
        # print(self.url_list)

    def begin_spider(self):
        with open('output/学工部&武装部.txt', 'w', encoding='utf-8') as fp:
            idx = 0
            for url in self.url_list:
                if idx % 100 == 0:
                    print(idx)
                title = ''
                time = ''
                text = ''
                try:
                    response = requests.get(url, self.headers, verify=False)
                except:
                    continue
                response.encoding = 'utf-8'
                selector = etree.HTML(response.text)
                title_list = selector.xpath('//div[@class="content-title"]/h3/text() |'
                                            '//div[@class="content-title1"]/h3/text()')
                time_list = selector.xpath('//div[@class="content-title"]/i/text() |'
                                           '//div[@class="content-title1"]/i/text()')
                text_list = selector.xpath('//div[@class="v_news_content"]/div/p/text() |'
                                           '//div[@class="v_news_content"]/p/text() |'
                                           '//div[@class="v_news_content"]/div/p/*/text() |'
                                           '//div[@class="v_news_content"]/p/*/text()')
                try:
                    for title_u in title_list:
                        title += title_u
                except:
                    pass
                try:
                    time_str = time_list[0]
                    time = re.findall(r"\d+-\d+-\d+", time_str)[0]
                except:
                    pass
                if len(text_list) == 0:
                    print(url)
                    continue
                for text_u in text_list:
                    text += text_u.strip()
                # print(title, time, text)
                fp.write(str(idx) + '|||' + title + '|||' + time + '|||' + url + '|||' + text.strip() + '\n')
                idx += 1


# type 3
class XiaoGongHui:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        self.max_count = 2490
        self.base_url = 'http://gh.ruc.edu.cn/displaynews.php?id='

    def begin_spider(self):
        with open('output/校工会.txt', 'w', encoding='utf-8') as fp:
            idx = 0
            for index in range(0, self.max_count + 1):
                if index % 100 == 0:
                    print(index)
                title = ''
                time = ''
                text = ''
                url = self.base_url + str(index)
                try:
                    response = requests.get(url, self.headers, verify=False)
                except:
                    continue
                response.encoding = 'utf-8'
                selector = etree.HTML(response.text)
                title_list = selector.xpath('//div[@class="sanshliulist"]/h1/text()')
                time_list = selector.xpath('//div[@class="sanshliulist"]/h2/text()')
                text_list = selector.xpath('//div[@class="sanshliulist"]/div/p/text() |'
                                           '//div[@class="sanshliulist"]/div/div/span/text() |'
                                           '//div[@class="sanshliulist"]/div/p/span/text() |'
                                           '//div[@class="sanshliulist"]/div/text() |'
                                           '//div[@class="sanshliulist"]/div/span/span/text() |'
                                           '//div[@class="sanshliulist"]/div/p/span/span/text() |'
                                           '//div[@class="sanshliulist"]/div/p/*/text() |'
                                           '//div[@class="sanshliulist"]/div/span/text() |'
                                           '//div[@class="sanshliulist"]/div/div/text()')

                try:
                    for title_u in title_list:
                        title += title_u
                except:
                    pass
                try:
                    time_str = time_list[0]
                    time = re.findall(r"\d+-\d+-\d+", time_str)[0]
                except:
                    pass
                if len(text_list) == 0:
                    print(url)
                    continue
                for text_u in text_list:
                    text += text_u.strip()
                if not text:
                    print(url)
                    continue
                fp.write(str(idx) + '|||' + title + '|||' + time + '|||' + url + '|||' + text.strip() + '\n')
                idx += 1


class FaZhanGuiHuaChu:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        self.max_count = 3116
        self.base_url = 'http://plan.ruc.edu.cn/Index/displaynews/id/'

    def begin_spider(self):
        with open('output/发展规划处.txt', 'w', encoding='utf-8') as fp:
            idx = 0
            for index in range(0, self.max_count + 1):
                if index % 100 == 0:
                    print(index)
                title = ''
                time = ''
                text = ''
                url = self.base_url + str(index) + '.html'
                try:
                    response = requests.get(url, self.headers, verify=False)
                except:
                    continue
                response.encoding = 'utf-8'
                selector = etree.HTML(response.text)
                title_list = selector.xpath('//div[@class="center clearf"]/div[@class="fr arti"]/h3/text()')
                time_list = selector.xpath('//span[@class="arti-time"]/text()')
                text_list = []
                try:
                    text_selector_list = selector.xpath('//p[@class="MsoNormal"]')
                except:
                    continue
                for text_selector in text_selector_list:
                    text_list += text_selector.xpath("string(.)")

                # text_list = selector.xpath('//p[@class="MsoNormal"]/text()')

                try:
                    for title_u in title_list:
                        title += title_u
                except:
                    pass
                try:
                    time_str = time_list[0]
                    time = re.findall(r"\d+-\d+-\d+", time_str)[0]
                except:
                    pass
                if len(text_list) == 0:
                    print(url)
                    continue
                for text_u in text_list:
                    text += text_u.strip()
                if not text:
                    print(url)
                    continue
                # print(url, title, time, text)
                fp.write(str(idx) + '|||' + title + '|||' + time + '|||' + url + '|||' + text.strip() + '\n')
                idx += 1


class ZhaoShengJiuYeChu:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        self.max_count = 150
        self.base_url = 'http://zsjyc.ruc.edu.cn/archives/'

    def begin_spider(self):
        with open('output/招生就业处.txt', 'w', encoding='utf-8') as fp:
            idx = 0
            for index in range(0, self.max_count + 1):
                if index % 100 == 0:
                    print(index)
                title = ''
                time = ''
                text = ''
                url = self.base_url + str(index)
                try:
                    response = requests.get(url, self.headers, verify=False)
                except:
                    continue
                response.encoding = 'utf-8'
                selector = etree.HTML(response.text)
                title_list = selector.xpath('//div[@class="col-md-9"]/h4[@class="title"]/text()')
                time_list = selector.xpath('//div[@class="col-md-9"]/p/span[2]/text()')
                try:
                    text_selector = selector.xpath('//div[@class="content"]')[0]
                except:
                    continue
                text_list = text_selector.xpath("string(.)")

                # text_list = selector.xpath('//p[@class="MsoNormal"]/text()')

                try:
                    for title_u in title_list:
                        title += title_u
                except:
                    pass
                try:
                    time_str = time_list[0]
                    time = re.findall(r"\d+-\d+-\d+", time_str)[0]
                except:
                    pass
                if len(text_list) == 0:
                    print(url)
                    continue
                for text_u in text_list:
                    text += text_u.strip()
                if not text:
                    print(url)
                    continue
                # print(url, title, time, text)
                fp.write(str(idx) + '|||' + title + '|||' + time + '|||' + url + '|||' + text.strip() + '\n')
                idx += 1


class CaiWuChu:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        self.max_count = 2405
        self.base_url = 'https://fo.ruc.edu.cn/displaynews.php?id='

    def begin_spider(self):
        with open('output/财务处.txt', 'w', encoding='utf-8') as fp:
            idx = 0
            for index in range(0, self.max_count + 1):
                if index % 100 == 0:
                    print(index)
                title = ''
                time = ''
                text = ''
                url = self.base_url + str(index)
                try:
                    response = requests.get(url, self.headers, verify=False)
                except:
                    continue
                response.encoding = 'utf-8'
                selector = etree.HTML(response.text)
                title_list = selector.xpath('//div[@class="title"]/h1/text()')
                time_list = selector.xpath('//div[@class="title"]/h2/text()')
                try:
                    text_selector = selector.xpath('//div[@class="paragraph"]')[0]
                except:
                    continue
                text_list = text_selector.xpath("string(.)")

                # text_list = selector.xpath('//p[@class="MsoNormal"]/text()')

                try:
                    for title_u in title_list:
                        title += title_u
                except:
                    pass
                try:
                    time_str = time_list[0]
                    time = re.findall(r"\d+-\d+-\d+", time_str)[0]
                except:
                    pass
                if len(text_list) == 0:
                    print(url)
                    continue
                for text_u in text_list:
                    text += text_u.strip()
                if not text or not title:
                    print(url)
                    continue
                # print(url, title, time, text)
                fp.write(str(idx) + '|||' + title + '|||' + time + '|||' + url + '|||' + text.strip() + '\n')
                idx += 1


class XiaoYouHui:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        self.max_count = 3150
        self.base_url = 'http://alumni.ruc.edu.cn/archives/'

    def begin_spider(self):
        with open('output/校友会.txt', 'w', encoding='utf-8') as fp:
            idx = 0
            for index in range(0, self.max_count + 1):
                if index % 100 == 0:
                    print(index)
                title = ''
                time = ''
                text = ''
                url = self.base_url + str(index)
                try:
                    response = requests.get(url, self.headers, verify=False)
                except:
                    continue
                response.encoding = 'utf-8'
                selector = etree.HTML(response.text)
                try:
                    title_list = selector.xpath('//div[@class="news-default-head"]/h6/text()')
                    time_list = selector.xpath('//div[@class="news-up"]/span[1]/text()')
                    text_selector = selector.xpath('//div[@class="news-default-content"]')[0]
                except:
                    continue
                text_list = text_selector.xpath("string(.)")

                # text_list = selector.xpath('//p[@class="MsoNormal"]/text()')

                try:
                    for title_u in title_list:
                        title += title_u
                except:
                    pass
                try:
                    time_str = time_list[0]
                    time = re.findall(r"\d+-\d+-\d+", time_str)[0]
                except:
                    pass
                if len(text_list) == 0:
                    print(url)
                    continue
                for text_u in text_list:
                    text += text_u.strip()
                if not text or not title:
                    print(url)
                    continue
                # print(url, title, time, text)
                fp.write(str(idx) + '|||' + title + '|||' + time + '|||' + url + '|||' + text.strip() + '\n')
                idx += 1


class KeYanChu:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        self.max_count = 4300
        self.base_url = 'http://keyan.ruc.edu.cn/index.php?s=/Index/news_cont_de/cid/'

    def begin_spider(self):
        with open('output/科研处.txt', 'w', encoding='utf-8') as fp:
            idx = 0
            for index in range(0, self.max_count + 1):
                if index % 100 == 0:
                    print(index)
                title = ''
                time = ''
                text = ''
                text_list = []
                url = self.base_url + str(index) + '.html'
                try:
                    response = requests.get(url, self.headers, verify=False)
                except:
                    print('1', url)
                    continue
                response.encoding = 'utf-8'
                selector = etree.HTML(response.text)
                title_list = selector.xpath('//div[@class="text_conment"]/h3/text()')
                time_list = selector.xpath('//div[@class="text_conment"]/p[@class="xs_data"]/text()')
                try:
                    text_selector_list = selector.xpath('//div[@class="text_conment"]/p')
                    for i in range(2, len(text_selector_list)):
                        text_list += text_selector_list[i].xpath("string(.)")
                except:
                    print('2', url)
                    continue
                # text_list = selector.xpath('//p[@class="MsoNormal"]/text()')

                try:
                    for title_u in title_list:
                        title += title_u
                except:
                    pass
                try:
                    time_str = time_list[0]
                    time = re.findall(r"\d+.\d+.\d+", time_str)[0]
                    time = time.replace('.', '-')
                except:
                    pass
                if len(text_list) == 0:
                    print('3', url)
                    continue
                for text_u in text_list:
                    text += text_u.strip()
                if not text or not title:
                    print('3', url)
                    continue
                # print(url, title, time, text)
                fp.write(str(idx) + '|||' + title + '|||' + time + '|||' + url + '|||' + text.strip() + '\n')
                idx += 1


class LiGongXueKeJianSheChu:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        self.max_count = 1350
        self.base_url = 'http://se-office.ruc.edu.cn/displaynews.php?id='

    def begin_spider(self):
        with open('output/理工学科建设处.txt', 'w', encoding='utf-8') as fp:
            idx = 0
            for index in range(0, self.max_count + 1):
                if index % 100 == 0:
                    print(index)
                title = ''
                time = ''
                text = ''
                url = self.base_url + str(index) + '.html'
                try:
                    response = requests.get(url, self.headers, verify=False)
                except:
                    continue
                response.encoding = 'utf-8'
                selector = etree.HTML(response.text)
                title_list = selector.xpath('//section[@class="biaoti"]/h5/text()')
                time_list = selector.xpath('//section[@class="biaoti"]/span/text()')
                try:
                    text_selector = selector.xpath('//ul[@class="cut"]/li')[0]
                except:
                    continue
                text_list = text_selector.xpath("string(.)")

                # text_list = selector.xpath('//p[@class="MsoNormal"]/text()')

                try:
                    for title_u in title_list:
                        title += title_u
                except:
                    pass
                try:
                    time_str = time_list[0]
                    time = re.findall(r"\d+-\d+-\d+", time_str)[0]
                except:
                    pass
                if len(text_list) == 0:
                    print(url)
                    continue
                for text_u in text_list:
                    text += text_u.strip()
                if not text or not title:
                    print(url)
                    continue
                # print(url, title, time, text)
                fp.write(str(idx) + '|||' + title + '|||' + time + '|||' + url + '|||' + text.strip() + '\n')
                idx += 1


class GuoJiJiaoLiuChu:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        self.max_count = 4858
        self.base_url = 'http://io.ruc.edu.cn/displaynews.php?id=100'

    def begin_spider(self):
        with open('output/国际交流处.txt', 'w', encoding='utf-8') as fp:
            idx = 0
            for index in range(0, self.max_count + 1):
                if index % 100 == 0:
                    print(index)
                title = ''
                time = ''
                text = ''
                text_list = []
                url = self.base_url + str(index).zfill(4)
                try:
                    response = requests.get(url, self.headers, verify=False)
                except:
                    print('1', url)
                    continue
                response.encoding = 'utf-8'
                selector = etree.HTML(response.text)
                title_list = selector.xpath('//div[@class="sider"]/h1/text()')
                time_list = selector.xpath('//div[@class="sider"]/h2/text()')
                try:
                    text_selector_list = selector.xpath('//div[@class="countiner"]/p')
                    for text_selector in text_selector_list:
                        text_list += text_selector.xpath("string(.)")
                except:
                    print('2', url)
                    continue
                # text_list = selector.xpath('//p[@class="MsoNormal"]/text()')

                try:
                    for title_u in title_list:
                        title += title_u
                except:
                    pass
                try:
                    time_str = time_list[0]
                    time = re.findall(r"\d+.\d+.\d+", time_str)[0]
                    time = time.replace('.', '-')
                except:
                    pass
                if len(text_list) == 0:
                    print('3', url)
                    continue
                for text_u in text_list:
                    text += text_u.strip()
                if not text or not title:
                    print('3', url)
                    continue
                # print(url, title, time, text)
                fp.write(str(idx) + '|||' + title + '|||' + time + '|||' + url + '|||' + text.strip() + '\n')
                idx += 1


class YanJiuShengYuan:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        self.max_count = 1787
        self.base_url_list = ['http://grs.ruc.edu.cn/info/1033/',
                              'http://grs.ruc.edu.cn/info/1034/',
                              'http://grs.ruc.edu.cn/info/1017/',
                              'http://grs.ruc.edu.cn/info/1018/',
                              'http://grs.ruc.edu.cn/info/1011/']

    def begin_spider(self):
        with open('output/研究生院.txt', 'w', encoding='utf-8') as fp:
            idx = 0
            for base_url in self.base_url_list:
                for index in range(0, self.max_count + 1):
                    if index % 100 == 0:
                        print(index)
                    title = ''
                    time = ''
                    text = ''
                    url = base_url + str(index) + '.htm'
                    try:
                        response = requests.get(url, self.headers, verify=False)
                    except:
                        print('1', url)
                        continue
                    response.encoding = 'utf-8'
                    selector = etree.HTML(response.text)
                    title_list = selector.xpath('//div[@class="tit-1y"]/h1/text()')
                    time_list = selector.xpath('//div[@class="info-1y"]/span[@class="time"]/em/text()')
                    try:
                        text_selector = selector.xpath('//div[@class="v_news_content"]')[0]
                        text_list = text_selector.xpath("string(.)")
                    except:
                        print('2', url)
                        continue
                    # text_list = selector.xpath('//p[@class="MsoNormal"]/text()')

                    try:
                        for title_u in title_list:
                            title += title_u
                    except:
                        pass
                    try:
                        time_str = time_list[0]
                        time = re.findall(r"\d+.\d+.\d+", time_str)[0]
                        time = time.replace('.', '-')
                    except:
                        pass
                    if len(text_list) == 0:
                        print('3', url)
                        continue
                    for text_u in text_list:
                        text += text_u.strip()
                    if not text or not title:
                        print('3', url)
                        continue
                    print(url, title, time, text)
                    # fp.write(str(idx) + '|||' + title + '|||' + time + '|||' + url + '|||' + text.strip() + '\n')
                    idx += 1


if __name__ == '__main__':
    spider = XiaoYouHui()
    # spider.get_url_list()
    spider.begin_spider()


