# -*- coding: utf-8 -*-
# @Time    : 2019/6/6 11:07
# @Author  : Shanlei Mu
# @Email   : msl@ruc.edu.cn
# @File    : return_result.py

import configparser
from .diversify import GetCaption


class ReturnResult:

    def __init__(self, config_path, config_encoding):
        self.config_path = config_path
        self.config_encoding = config_encoding
        config = configparser.ConfigParser()
        config.read(config_path, config_encoding)
        self.doc_file = config['DEFAULT']['content_data_path']
        self.doc_dict = {}  # key: docid, value: [docid, title, date, url, text]

    def load_doc(self):
        print('loading doc file...')
        with open(self.doc_file, 'r', encoding='utf-8') as fp:
            for line in fp:
                line_splited = line.strip().split('|||')
                docid = line_splited[0]
                title = line_splited[1]
                date = line_splited[2]
                url = line_splited[3]
                text = line_splited[4]
                self.doc_dict[docid] = [docid, title, date, url, text]

    def return_result(self, flag, bm25_scores, cleaned_dict):
        result_list = []
        for score in bm25_scores:
            docid = score[0]
            result_list.append(self.doc_dict[docid])

        captions = GetCaption(self.doc_dict, bm25_scores, cleaned_dict.keys())
        return flag, result_list, captions
