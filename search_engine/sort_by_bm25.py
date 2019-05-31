# -*- coding: utf-8 -*-
# @Time    : 2019/5/29 19:52
# @Author  : Shanlei Mu
# @Email   : msl@ruc.edu.cn
# @File    : sort_by_bm25.py

"""
bm25算法
"""

import jieba
import math
import configparser


class SearchEngine:
    def __init__(self, config_path, config_encoding):
        self.config_path = config_path
        self.config_encoding = config_encoding
        config = configparser.ConfigParser()
        config.read(config_path, config_encoding)
        f = open(config['DEFAULT']['stop_words_path'], encoding = config['DEFAULT']['stop_words_encoding'])
        words = f.read()
        self.stop_words = set(words.split('\n'))
        self.index_file = config['DEFAULT']['index_output_path']
        self.doc_file = config['DEFAULT']['content_data_path']
        self.K1 = float(config['DEFAULT']['k1'])
        self.B = float(config['DEFAULT']['b'])
        self.N = int(config['DEFAULT']['n'])
        self.AVG_L = float(config['DEFAULT']['avg_l'])
        self.reverse_index_dict = {}
        self.doc_dict = {}

    def read_reverse_index(self):
        print('loading reverse index...')
        with open(self.index_file, 'r') as fp:
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

    def read_doc(self):
        print('loading doc file...')
        with open(self.doc_file, 'r') as fp:
            for line in fp:
                docid = line.strip().split('|||')[0]
                self.doc_dict[docid] = line

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def clean_list(self, seg_list):
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

    def result_by_BM25(self, sentence):
        seg_list = jieba.lcut(sentence, cut_all=False)
        n, cleaned_dict = self.clean_list(seg_list)
        BM25_scores = {}
        for term in cleaned_dict.keys():
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
                if docid in BM25_scores:
                    BM25_scores[docid] = BM25_scores[docid] + s
                else:
                    BM25_scores[docid] = s
        BM25_scores = sorted(BM25_scores.items(), key=lambda d: d[1], reverse=True)
        if len(BM25_scores) == 0:
            return 0, []
        else:
            return 1, BM25_scores

    def search(self, sentence):
        flag, rs = self.result_by_BM25(sentence)
        for r in rs[:5]:
            print(self.doc_dict[r[0]])


if __name__ == '__main__':
    se = SearchEngine('../config.ini', 'utf-8')
    se.read_reverse_index()
    se.read_doc()
    while True:
        se.search(input('query: '))
