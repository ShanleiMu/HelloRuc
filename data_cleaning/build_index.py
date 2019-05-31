# -*- coding: utf-8 -*-
# @Time    : 2019/5/29 15:14
# @Author  : Shanlei Mu
# @Email   : msl@ruc.edu.cn
# @File    : data_cleaning.py

import jieba
import configparser


class Doc:
    docid = 0
    date_time = ''
    tf = 0
    ld = 0

    def __init__(self, docid, date_time, tf, ld):
        self.docid = docid
        self.date_time = date_time
        self.tf = tf
        self.ld = ld

    def __repr__(self):
        return (str(self.docid) + '\t' + self.date_time + '\t' + str(self.tf) + '\t' + str(self.ld))

    def __str__(self):
        return (str(self.docid) + '\t' + self.date_time + '\t' + str(self.tf) + '\t' + str(self.ld))


class IndexModule:

    def __init__(self, config_path, config_encoding):
        self.config_path = config_path
        self.config_encoding = config_encoding
        config = configparser.ConfigParser()
        config.read(config_path, config_encoding)
        f = open(config['DEFAULT']['stop_words_path'], encoding=config['DEFAULT']['stop_words_encoding'])
        words = f.read()
        self.stop_words = set(words.split('\n'))
        self.postings_lists = {}

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

    def construct_postings_lists(self):
        config = configparser.ConfigParser()
        config.read(self.config_path, self.config_encoding)
        data_file = config['DEFAULT']['content_data_path']

        AVG_L = 0
        with open(data_file, 'r') as fp:
            doc_count = 0
            for line in fp:
                doc_count += 1
                if doc_count % 1000 == 0:
                    print(doc_count)
                line_splited = line.strip().split('|||')
                docid = line_splited[0]
                title = line_splited[1]
                date_time = line_splited[2]
                body = line_splited[4]
                seg_list = jieba.lcut(title + '。' + body, cut_all=False)
                ld, cleaned_dict = self.clean_list(seg_list)
                AVG_L = AVG_L + ld

                for key, value in cleaned_dict.items():
                    d = Doc(docid, date_time, value, ld)
                    if key in self.postings_lists:
                        self.postings_lists[key][0] = self.postings_lists[key][0] + 1  # df++
                        self.postings_lists[key][1].append(d)
                    else:
                        self.postings_lists[key] = [1, [d]]  # [df, [Doc]]
        AVG_L = AVG_L / doc_count
        config.set('DEFAULT', 'N', str(doc_count))
        config.set('DEFAULT', 'avg_l', str(AVG_L))
        with open(self.config_path, 'w', encoding=self.config_encoding) as configfile:
            config.write(configfile)
        output_file = config['DEFAULT']['index_output_path']
        with open(output_file, 'w') as fo:
            for term in self.postings_lists:
                outline = term + '$' + str(self.postings_lists[term][0]) + '$'
                for doc in self.postings_lists[term][1]:
                    outline += str(doc.docid) + '\t' + str(doc.date_time) + '\t' \
                               + str(doc.tf) + '\t' + str(doc.ld) + '|'
                outline += '\n'
                fo.write(outline)


if __name__ == "__main__":
    im = IndexModule('../config.ini', 'utf-8')
    im.construct_postings_lists()
