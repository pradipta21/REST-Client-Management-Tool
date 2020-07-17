# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 14:28:44 2020

@author: pradipta.s
"""
import re

str = "avc:sss,ppp:111,jvc:po"
print(re.findall('[a-z]+:',str))
print(str.replace(r'[a-z]+:',"aaa."))