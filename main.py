# -*- coding: utf-8 -*-
# @Time    : 2019/5/31 17:44
# @Author  : Shanlei Mu
# @Email   : msl@ruc.edu.cn
# @File    : main.py

from search_engine.sort_by_bm25 import SearchEngine


if __name__ == '__main__':
    se = SearchEngine('../config.ini', 'utf-8')
    se.read_reverse_index()
    se.read_doc()
    while True:
        se.search(input('query: '))
