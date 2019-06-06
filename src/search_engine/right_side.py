# -*- coding: utf-8 -*-
# @Time    : 2019/6/4
# @Author  : GarfieldWong
# @Email   : wangshijun@ruc.edu.cn
# @File    : right_side.py

"""
动态计算，得到显示到搜索结果页右侧的东西
从不多于10条的 显示在左侧的 搜索结果 中找信息

相关人物、相关官网

needs:
doc_dict: {'docid': 'docline', ...}
relevant scores: [('docid', score), ...] # sorted
"""

import fool
from collections import Counter


def get_right_side(doc_dict: dict, rs: list):
    """
    find relevant person and relevant school from results showed on the left
    args:
        doc_dict: dict, {'docid': 'docline', ...}
        rs: sorted list, [('docid', score), ...]
            len(rs) <= 10
    return:
        person: a Counter of relevant person
        org: a Counter of relevant school 
    """
    person_list = list()
    org_list = list()
    for docid, _score in rs:
        doc_line = doc_dict[docid]
        _docid, doc_title, _doc_date, _doc_url, doc_text = doc_line.split('|||')
        _words, ners = fool.analysis([doc_title, doc_text])
        ners = ners[0] + ners[1]
        person_list.extend([t4[3] for t4 in ners if t4[2] == 'person'])
        org_list.extend([t4[3] for t4 in ners if t4[2] == 'org'])
    # print(Counter(person_list))
    # print(Counter(org_list))
    return Counter(person_list), Counter(org_list)