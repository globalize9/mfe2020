# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 14:55:29 2019

@author: yushi
"""


import math
import os
import random
import re
import sys
import datetime as dt

# Complete the time_delta function below.
def time_delta(t1, t2):
    t1aa = dt.datetime.strptime(t1, '%a %d %B %Y %H:%M:%S %z')
    t2aa = dt.datetime.strptime(t2, '%a %d %B %Y %H:%M:%S %z')

    return(int(abs((t1aa-t2aa).total_seconds())))



t = int(input())
secondsArr = [None] * t
for t_itr in range(t):
        t1 = input()
        t2 = input()
        secondsArr[t_itr] = time_delta(t1,t2)
        print(secondsArr[t_itr])