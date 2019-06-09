# -*- coding: utf-8 -*-
# @Time    : 2019/6/5 11:46
# @Author  : Shanlei Mu
# @Email   : msl@ruc.edu.cn
# @File    : main.py

from src.data_cleaning.IndexModule import IndexModule
from src.search_engine.right_side import Relevant


if __name__ == '__main__':
    im = IndexModule('config.ini', 'utf-8')
    im.construct_postings_lists()
    # r = Relevant()
    # org_dict = r.relevant_org
    # person_dict = r.relevant_person
    # org_set = set()
    # for docid in org_dict:
    #     for org in org_dict[docid]:
    #         org = org.strip()
    #         if org not in org_set:
    #             org_set.add(org)
    # print(len(org_set))
    #
    # person_set = set()
    # for docid in person_dict:
    #     for person in person_dict[docid]:
    #         person = person.strip()
    #         if person not in person_set:
    #             person_set.add(person)
    # print(len(person_set))
    #
    # with open('src/data/org.txt', 'w', encoding='utf-8') as fo:
    #     for org in org_set:
    #         fo.write(org + '\n')
    #     for person in person_set:
    #         fo.write(person + '\n')
