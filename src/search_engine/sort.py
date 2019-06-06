# -*- coding: utf-8 -*-
# @Time    : 2019/5/29 19:52
# @Author  : Shanlei Mu
# @Email   : msl@ruc.edu.cn
# @File    : sort.py

"""
检索算法
"""

import jieba
import math
import configparser
from datetime import *


class Sort:

    def __init__(self, config_path, config_encoding):
        self.config_path = config_path
        self.config_encoding = config_encoding
        config = configparser.ConfigParser()
        config.read(config_path, config_encoding)
        f = open(config['DEFAULT']['stop_words_path'], encoding=config['DEFAULT']['stop_words_encoding'])
        words = f.read()
        self.stop_words = set(words.split('\n'))
        self.index_file = config['DEFAULT']['index_output_path']
        self.K1 = float(config['DEFAULT']['k1'])
        self.B = float(config['DEFAULT']['b'])
        self.N = int(config['DEFAULT']['n'])
        self.AVG_L = float(config['DEFAULT']['avg_l'])
        self.reverse_index_dict = {}

    def load_reverse_index(self):
        print('loading reverse index...')
        with open(self.index_file, 'r', encoding='utf-8') as fp:
            for line in fp:
                line_splited_1 = line.strip().split('$')
                term = line_splited_1[0]
                df = line_splited_1[1]
                doc_list = line_splited_1[2].strip().split('|')[:-1]
                self.reverse_index_dict[term] = []
                self.reverse_index_dict[term].append(df)
                self.reverse_index_dict[term].append([])
                for doc in doc_list:
                    doc_attribute = doc.split('\t')
                    self.reverse_index_dict[term][1].append(doc_attribute)

    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def clean_list(self, seg_list):
        """
        对分词结果的list进行处理，返回词数n和清理后的词list
        """
        cleaned_dict = {}
        n = 0
        for i in seg_list:
            i = i.strip().lower()
            if i != '' and not self.is_number(i) and i not in self.stop_words:
                n = n + 1
                if i in cleaned_dict:
                    cleaned_dict[i] = cleaned_dict[i] + 1
                else:
                    cleaned_dict[i] = 1
        return n, cleaned_dict

    # 对排序结果进行重排来增加多样性
    # alpha控制重复学院分值下降速度， beta控制下限
    @staticmethod
    def diversify(sort_list):
        sid_list = {}
        alpha = 0.05
        beta = 0.8
        for i in range(len(sort_list)):
            sort_list[i] = list(sort_list[i])
            sid = sort_list[i][0][:3]
            if sid not in sid_list.keys():
                sid_list[sid] = 1
            else:
                sid_list[sid] += 1
            decay = (math.exp(-(sid_list[sid] - 1) * alpha)) * (1 - beta) + beta
            sort_list[i][1] = sort_list[i][1] * decay
        sort_list = sorted(sort_list, key=lambda d: d[1], reverse=True)
        return sort_list

    def result_by_bm25(self, query):
        """
        根据query进行检索，返回是否有结果和文档id list
        return结果 flag, bm25_scores: [(id, score),...,(id, score)]
        """
        seg_list = jieba.lcut(query, cut_all=False)
        n, cleaned_dict = self.clean_list(seg_list)
        print('cleaned_dict: ', cleaned_dict)
        bm25_scores = {}
        for term in cleaned_dict.keys():
            try:
                r = self.reverse_index_dict[term]
                if r is None:
                    continue
                df = int(r[0])
                w = math.log2((self.N - df + 0.5) / (df + 0.5))
                docs = r[1]
                for doc in docs:
                    docid = doc[0]
                    date_time = doc[1]
                    tf = doc[2]
                    ld = doc[3]
                    docid = docid
                    tf = int(tf)
                    ld = int(ld)
                    s = (self.K1 * tf * w) / (tf + self.K1 * (1 - self.B + self.B * ld / self.AVG_L))
                    if docid in bm25_scores:
                        bm25_scores[docid] = bm25_scores[docid] + s
                    else:
                        bm25_scores[docid] = s
            except KeyError:
                print('can not find ' + term + ' in reverse index')
        bm25_scores = sorted(bm25_scores.items(), key=lambda d: d[1], reverse=True)
        bm25_scores = self.diversify(bm25_scores)
        if len(bm25_scores) == 0:
            return 0, [], cleaned_dict
        else:
            return 1, bm25_scores, cleaned_dict

    def result_by_time(self, query):
        seg_list = jieba.lcut(query, cut_all=False)
        n, cleaned_dict = self.clean_list(seg_list)
        time_scores = {}
        for term in cleaned_dict.keys():
            try:
                r = self.reverse_index_dict[term]
                if r is None:
                    continue
                docs = r[1]
                for doc in docs:
                    docid = doc[0]
                    date_time = doc[1]
                    if docid in time_scores:
                        continue
                    try:
                        news_datetime = datetime.strptime(date_time, "%Y-%m-%d")
                        now_datetime = datetime.now()
                        td = now_datetime - news_datetime
                        td = float((timedelta.total_seconds(td) / 3600))   # hour
                    except ValueError:
                        td = 25000.00
                    time_scores[docid] = td
            except KeyError:
                print('can not find ' + term + ' in reverse index')
        time_scores = sorted(time_scores.items(), key=lambda d: d[1], reverse=False)
        print(time_scores)
        if len(time_scores) == 0:
            return 0, [], cleaned_dict
        else:
            return 1, time_scores, cleaned_dict

    def result_by_hot(self, query):
        seg_list = jieba.lcut(query, cut_all=False)
        n, cleaned_dict = self.clean_list(seg_list)
        print('cleaned_dict: ', cleaned_dict)
        hot_scores = {}
        word_count = {}
        max_count = len(cleaned_dict.keys())
        for term in cleaned_dict.keys():
            try:
                r = self.reverse_index_dict[term]
                if r is None:
                    continue
                df = int(r[0])
                w = math.log2((self.N - df + 0.5) / (df + 0.5))
                docs = r[1]
                for doc in docs:
                    docid = doc[0]
                    date_time = doc[1]
                    tf = doc[2]
                    ld = doc[3]
                    tf = int(tf)
                    ld = int(ld)
                    bm25_score = (self.K1 * tf * w) / (tf + self.K1 * (1 - self.B + self.B * ld / self.AVG_L))
                    try:
                        news_datetime = datetime.strptime(date_time, "%Y-%m-%d")
                        now_datetime = datetime.strptime('2019-05-28', "%Y-%m-%d")
                        td = now_datetime - news_datetime
                        td = float((timedelta.total_seconds(td) / 3600))   # hour
                    except ValueError:
                        td = 25000.00
                    bm25_score = math.log(bm25_score + 1)
                    time_score = 1 / (td + 100)
                    hot_score = bm25_score + time_score
                    if docid in hot_scores:
                        hot_scores[docid] = hot_scores[docid] + hot_score
                        word_count[docid] += 1
                    else:
                        hot_scores[docid] = hot_score
                        word_count[docid] = 1
            except KeyError:
                print('can not find ' + term + ' in reverse index')
        for doc in word_count:
            if word_count[doc] < max_count:
                hot_scores.pop(doc)
        hot_scores = sorted(hot_scores.items(), key=lambda d: d[1], reverse=True)
        if len(hot_scores) < 10:
            print(hot_scores)
        else:
            print(hot_scores[:10])
        # hot_scores = self.diversify(hot_scores)
        if len(hot_scores) == 0:
            return 0, [], cleaned_dict
        else:
            return 1, hot_scores, cleaned_dict