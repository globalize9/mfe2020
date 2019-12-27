# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 20:09:38 2019

@author: yushi
"""

# Complete the 'rotateTheString' function below.
#
# The function is expected to return a STRING.
# The function accepts following parameters:
#  1. STRING originalString
#  2. INTEGER_ARRAY direction
#  3. INTEGER_ARRAY amount
#

def rotateTheString(originalString = "", direction = [0, 0], amount = [3,4]):
    # Write your code here
    samplestr = "isrightbenny"
    split_str = [char for char in samplestr]
    new = originalString

    def rotateRight(split_str):
        temp = [char for char in split_str]
        del(temp[0])
        temp_2 = temp + [split_str[0]]
        newStr = []
        for i in range(len(temp_2)):
            newStr.append(temp_2[i])
        return (''.join(newStr))

    def rotateLeft(split_str):
        temp = [char for char in split_str]
        del(temp[len(split_str)-1])
        temp_2 = [split_str[len(split_str)-1]] + temp
        newStr = []
        for i in range(len(temp_2)):
            newStr.append(temp_2[i])
        return (''.join(newStr))
    new = "isrightbenny"
    for i in range(len(direction)):
        #for i in range(len(amount)):
        j = i
        for z in range(amount[i]):
            if (direction[i] == 0):
                new = rotateRight(new)
            if (direction[i] == 1):
                new = rotateLeft(new)
    print(new)
    return(new)

'''if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    originalString = input()

    direction_count = int(input().strip())

    direction = []

    for _ in range(direction_count):
        direction_item = int(input().strip())
        direction.append(direction_item)

    amount_count = int(input().strip())

    amount = []

    for _ in range(amount_count):
        amount_item = int(input().strip())
        amount.append(amount_item)

    result = rotateTheString(originalString, direction, amount)

    fptr.write(result + '\n')

    fptr.close()'''

# 1
word = 'abcd'

#def rotate(org, direction, amount):
#    x = org.split()
#    index = list(range(len(x)))
#    xnew = []
#    indexnew=[]
#    for dir in direction:
#
#            if dir == 0: #left
#                for i in index:
#                    indexnew.append(i-1)
#
#                for i in indexnew:
#                    if i < 0:
#                        i = len(x) - i
#
#                    xnew.append(x[i-1])
#            elif item == 1: #right

word = 'isrightbenny'
direction = [0,0] #left, right
movement = [3,4] #once, twice = right once

def rotateTheStringMina(originalString = word, direction = direction, amount = movement):
    x = originalString.split()
    index = list(range(len(x)))

    x = list(originalString)
    index = list(range(len(x)))

    for i in range(len(direction)):
        d = direction[i]
        m = amount[i]
        count = 0
        while count < m:
            if d == 0: #left
                indexnew = [item-1 for item in index]
                for t in range(len(indexnew)):
                    if indexnew[t]<0:
                        indexnew[t] = len(x) + indexnew[t]
                    index[t] = indexnew[t]

            elif d == i: #right
                indexnew = [item+1 for item in index]
                for t in range(len(indexnew)):
                    if indexnew[t] > (len(x)-1):
                        indexnew[t] = len(x) - indexnew[t]
                    index[t] = indexnew[t]

            count += 1


    arr=[0 for x in range(len(x))]
    for i in range(len(x)):
        tempindex = indexnew[i]
        a = x[i]
        arr[tempindex] = a

    new = ""
    for i in arr:
        new += i

    return(new)

print(rotateTheString())




