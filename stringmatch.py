# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 13:21:35 2019

@author: yushi
"""

#s = "zzzxxxzzz"

#cutoff = 2
#s1 = s[0:cutoff]
#s2 = s[cutoff:len(s)]

def counter(strA, strB):
    s1 = [x for x in strA]
    s2 = [x for x in strB]
    counter = []

    for i in range(len(s1)):
        temp = 0
        for j in range(len(s2)):
            if (s1[i] == s2[j]):
                temp += 1
                del(s2[j])
                break
        counter.append(temp)
    return(sum(counter))

word = 'abcdedeara'
word = 'zzzxxxzzz'

sep = list(word)
n = len(sep)
result = []

for i in range(1,len(sep)): # how many ways
    a = []
    b = []
    for t in range(i):
        a.append(sep[t])
    for comp in range(i,n):
        b.append(sep[comp])

    result.append(counter(a,b))
    maxnumber = -999
    for items in result:
        if (items > maxnumber):
            maxnumber = items

#print(maxnumber)





