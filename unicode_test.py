#!/usr/bin/env python\
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 15 14:21:33 2015

@author: Brian Sandberg
"""


u = 'idzie wąż wąską dróżką'
uu = u.decode('utf8')
s = uu.encode('cp1250')
print(s)