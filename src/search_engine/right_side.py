# -*- coding: utf-8 -*-
# @Time    : 2019/6/8
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

import re
import json
import time
import fool
import configparser
from collections import Counter

# this class is the only thing that can be imported from outside this file
class Relevant(object):
    
    def __init__(self, relevant_things_path="src/data/processed_data/ruc_relevant_things.json"):
        """
        relevant_person: dict, {'docid': {'person': num shown, ...}, ...}
        relevant_org: dict, {'docid': {'org': num shown, ...}, ...}
        """
        self.url_prefix = "https://www.baidu.com/s?wd=" # + "person_name/org_name"
        f = open(relevant_things_path, 'r', encoding='utf-8')
        self.relevant_person, self.relevant_org = json.load(f)
        f.close()

    def get_relevant_person(self, scores: list):
        """
        havn't decide the weighting method yet
        using unweighted method now, means each item in scores(list) viewed the same
        args:
            scores: sorted list, [('docid', score), ...], suggested length <= 10
        return:
            a sorted list of ('relevant person name', num shown)
        """
        person = dict()
        for docid, _score in scores[:10]:
            for p, num in self.relevant_person[docid].items():
                if p in person:
                    person[p] += num
                else:
                    person[p] = num
        return sorted(person.items(), key=lambda k: k[1], reverse=True)
    
    def get_relevant_org(self, scores: list):
        """
        havn't decide the weighting method yet
        using unweighted method now, means each item in scores(list) viewed the same
        args:
            scores: sorted list, [('docid', score), ...], suggested length <= 10
        return:
            a sorted list of ('relevant organization name', num shown)
        """
        org = dict()
        for docid, _score in scores[:10]:
            for o, num in self.relevant_org[docid].items():
                if o in org:
                    org[o] += num
                else:
                    org[o] = num
        return sorted(org.items(), key=lambda k: k[1], reverse=True)

    def get_relevant_person_with_url(self, scores: list):
        """
        args:
            scores: sorted list, [('docid', score), ...], suggested length <= 10
        return:
            a list of ('relevant person name', 'url')
            'relevant person name' is sorted
        """
        person_score_list = self.get_relevant_person(scores)
        person_url_list = [(person_name, self.url_prefix + person_name) for person_name, _score in person_score_list]
        return person_url_list

    def get_relevant_org_with_url(self, scores: list):
        """
        args:
            scores: sorted list, [('docid', score), ...], suggested length <= 10
        return:
            a list of ('relevant org name', 'url')
            'relevant org name' is sorted
        """
        org_score_list = self.get_relevant_org(scores)
        org_url_list = [(org_name, self.url_prefix + org_name) for org_name, _score in org_score_list]
        return org_url_list

# discarded
def get_right_side_dynamic(doc_dict: dict, rs: list):
    """
    find relevant person and relevant organization from results showed on the left
    args:
        doc_dict: dict, {'docid': 'docline', ...}
        rs: sorted list, [('docid', score), ...]
            len(rs) <= 10
    return:
        person: a Counter of relevant person
        org: a Counter of relevant organization 
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

def get_all_relevant_things(doc_dict: dict):
    """
    find relevant person and relevant organization for all docs
    args:
        doc_dict: dict, {'docid': 'docline', ...}
    return:
        relevant_person: dict, {'docid': {'person': num shown, ...}, ...}
        relevant_org: dict, {'docid': {'org': num shown, ...}, ...}
    """
    relevant_person = dict()
    relevant_org = dict()
    c = 0
    for docid in doc_dict:
        c += 1
        if c % 500 == 0:
            print(c, "docs done at", time.asctime(time.localtime(time.time())))
        doc_line = doc_dict[docid]
        _docid, doc_title, _doc_date, _doc_url, doc_text = doc_line.split('|||')
        _words, ners = fool.analysis([doc_title, doc_text])
        ners = ners[0] + ners[1]
        person_list = [t4[3] for t4 in ners if t4[2] == 'person']
        org_list = [t4[3] for t4 in ners if t4[2] == 'org']
        relevant_person[docid] = Counter(person_list)
        relevant_org[docid] = Counter(org_list)
    return relevant_person, relevant_org

def save_all_relevant_things(doc_dict: dict, config):
    """
    save relevant person and relevant organization for all docs
    args:
        doc_dict: dict, {'docid': 'docline', ...}
    return:
        nothing
    """
    relevant_person, relevant_org = get_all_relevant_things(doc_dict)
    print("start saving at", time.asctime(time.localtime(time.time())))
    with open(config['DEFAULT']['relevant_things'], 'w', encoding='utf-8') as f:
        json.dump([relevant_person, relevant_org], f)
    return

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini', 'utf-8')
    # doc_dict = dict()
    # with open(config['DEFAULT']['content_data_path'], 'r', encoding='utf-8') as f:
    #     for line in f:
    #         docid = line.split('|||')[0]
    #         doc_dict[docid] = line
    # print("finished loading doc_dict at", time.asctime(time.localtime(time.time())))
    # save_all_relevant_things(doc_dict, config)
    # relevant_person, relevant_org = load_all_relevant_things(config['DEFAULT']['relevant_things'])
    re = Relevant(config['DEFAULT']['relevant_things'])
    # re.relevant_person, re.relevant_org