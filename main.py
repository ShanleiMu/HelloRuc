# -*- coding: utf-8 -*-
# @Time    : 2019/6/5 11:46
# @Author  : Shanlei Mu
# @Email   : msl@ruc.edu.cn
# @File    : main.py

from src.data_cleaning.IndexModule import IndexModule


if __name__ == '__main__':
    im = IndexModule('config.ini', 'utf-8')
    im.construct_postings_lists()
