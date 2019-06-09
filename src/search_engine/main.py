# -*- coding: utf-8 -*-
# @Time    : 2019/5/31 17:44
# @Author  : Shanlei Mu
# @Email   : msl@ruc.edu.cn
# @File    : main.py

from .sort import Sort
from .return_result import ReturnResult
from .correction import Corrector

se = Sort('config.ini', 'utf-8')
rs = ReturnResult('config.ini', 'utf-8')
co = Corrector('config.ini', 'utf-8')
