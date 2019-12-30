# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 10:07:18 2019

@author: yushi
"""

mapping = [3,5,4,6,2,7,9,8,0]
nums = ['990','332','32']
match = []

def matchpoint(match):
    nums = [x for x in match]
    result = []
    gg = []

    for item in nums:
        sep = list(item)
        s_list = []
        for k in range(len(sep)):
            temp = mapping[sep[k]]
            s_list.append(temp)
        result.append(s_list)

    for z in result:
        temp_str = ""
        for i in range(len(z)):
            temp_str += str(z[i])
        gg.append(temp_str)

    return(gg)

for item in nums:
    sep = list(item)
    index = [mapping.index(int(letter)) for letter in sep]
    match.append(index)

converted = [x for x in match]
for i in range(len(match)):
    group = match[i]
    temp = ''
    for item in group:
        temp += str(item)
    converted[i] = int(temp)

match.sort()

matchpoint(match)
    '''for item in nums:
        sep = list(item)
        actual = [mapping.index(int(letter)) for letter in sep]
        for i in range(len(nums)):
            mw = []
            for j in range(len(nums[i])):
                temp = mapping[nums[i][j]]
                mw.append(temp)
            result.append(mw[i])
        #result.append(actual)'''

def matchpoint(match,mapping):
    nums = [x for x in match]
    result = []
    gg = []

    for item in nums:
        sep = list(item)
        s_list = []
        for k in range(len(sep)):
            temp = mapping[sep[k]]
            s_list.append(temp)
        result.append(s_list)

    for z in result:
        temp_str = ""
        for i in range(len(z)):
            temp_str += str(z[i])
        gg.append(temp_str)

    return(gg)

def strangeSort(mapping, nums):
    match  = []
    for item in nums:
        sep = list(item)
        index = [mapping.index(int(letter)) for letter in sep]
        match.append(index)

    converted = [x for x in match]
    for i in range(len(match)):
        group = match[i]
        temp = ''
        for item in group:
            temp += str(item)
        converted[i] = int(temp)

    match.sort()
    return(matchpoint(match,mapping))