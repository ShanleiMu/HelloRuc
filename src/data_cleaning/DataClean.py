# -*- coding: utf-8 -*-
# @Time    : 2019/5/29 14:36
# @Author  : Shanlei Mu
# @Email   : msl@ruc.edu.cn
# @File    : DataClean.py

import os.path
import re
from datetime import *


class DataClean:

    def traverse_file(self, file_path):
        path_dir = os.listdir(file_path)
        file_list = []
        for all_dir in path_dir:
            child = os.path.join('%s/%s' % (file_path, all_dir))
            if os.path.isfile(child):
                file_list.append(child)
                continue
            file_list.extend(self.traverse_file(child))
        return file_list

    def count_data_number(self, list_of_file):
        count_sum = 0
        for file in list_of_file:
            with open(file, 'r', encoding='utf-8') as fp:
                count = len(fp.readlines())
                print(file, count)
                count_sum += count
        return count_sum

    def clean_data(self, file_input, idx1):
        content_list = []
        with open(file_input, 'r') as fp:
            idx2 = 0
            for line in fp:
                line_splited = line.strip().split('|||')
                try:
                    index = line_splited[0].strip()
                    title = line_splited[1].strip()
                    time = line_splited[2].strip()
                    url = line_splited[3].strip()
                    text = line_splited[4].strip()
                except:
                    # print(line)
                    continue
                index_t = '\d+'
                time_t = '\d+-\d+-\d+'
                if not re.search(index_t, index):
                    continue
                if not re.search(time_t, time):
                    continue
                if not title:
                    continue
                if not text:
                    continue
                outline = str(idx1).zfill(3) + str(idx2).zfill(4) + '|||' \
                          + title + '|||' + time + '|||' + url + '|||' + text + '\n'
                content_list.append(outline)
                idx2 += 1
        return content_list

    def merge_data(self, list_of_file, output_file, index_file):
        with open(output_file, 'w') as fo, open(index_file, 'w') as fo1:
            index = 0
            for input_file in list_of_file:
                contents = self.clean_data(input_file, index)
                for line in contents:
                    fo.write(line)
                fo1.write(str(index).zfill(3) + '\t' + input_file.split('/')[-1] + '\n')
                index += 1

    def duplicate_removal(self, list_of_file):
        for file in list_of_file:
            with open(file, 'r') as fp, open('../data/distinct_data/' + file.split('/')[-1], 'w') as fo:
                idx1 = 0
                doc_set = set()
                for line in fp:
                    idx1 += 1
                    line_splited = line.strip().split('|||')
                    try:
                        title_time = line_splited[1] + line_splited[2]
                    except:
                        print(line)
                    if title_time not in doc_set:
                        fo.write(line)
                        doc_set.add(title_time)
                print(file, idx1, len(doc_set))

    @staticmethod
    def check_date(file):
        idx = 0
        with open(file, 'r', encoding='utf-8') as fp:
            for line in fp:
                idx += 1
                if idx % 1000 == 0:
                    print(idx)
                date = line.strip().split('|||')[2]
                try:
                    date = datetime.strptime(date, "%Y-%m-%d")
                except ValueError:
                    print(line)
                    new_date = re.findall(r"\d+-\d+-\d+", date)[0]
                    line = line.replace(date, new_date)


# if __name__ == '__main__':
#     file_list = traverse_file('../data/distinct_data')
#     # total_data = count_data_number(file_list)
#     # print('total data: ', total_data)
#     merge_data(file_list, '../data/processed_data/ruc_content.txt', '../data/department2index.txt')
#     # duplicate_removal(file_list)


if __name__ == '__main__':
    dc = DataClean()
    news_date = dc.check_date('../data/processed_data/ruc_content2.txt')
