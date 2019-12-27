# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 19:26:23 2019

@author: yushi
"""
import numpy as np


n = 6
matrix = np.zeros(shape=(n,n))

#for i in range(n):
 #   matrix[i,:] = list(map(int,input().split()))

matrix = ([1,1,1,0,0,0],
          [0,1,0,0,0,0],
          [1,1,1,0,0,0],
          [0,0,0,0,0,0],
          [0,0,0,0,0,0],
          [0,0,0,0,0,0])

nrow, ncol = np.shape(matrix)
total = []
for i in range(nrow):
    for j in range(ncol):
        if (i < nrow - 2 and j < ncol - 2):
            temp = matrix[i][j] + matrix[i][j+1] + matrix[i][j+2] + \
            matrix[i+1][j+1] + matrix[i+2][j] + matrix[i+2][j+1] + matrix[i+2][j+2]
            total.append(temp)
print(max(total))


# optimal path...goal to obtain the most point stcs
#intake = str(input())
intake = "1,-2,3,2,1;1,2,4,-8,2;2,1,6,4,3;3,-7,1,0,-4;4,3,2,2,1"
temp_1 = intake.split(";")
arr = []
for i in range(len(temp_1)):
    temp_20 = temp_1[i].split(",")
    temp_21 = []
    for j in range(len(temp_20)):
        temp_21.append(int(temp_20[j]))
    arr.append(temp_21)

arr

n = len(temp_1)
center = int((n-1)/2) # also corresponds to the total number of steps taken
top_left = []


# program based on walking with the lowest neighbours, 1/4 quadrants
i = 0
j = 0
move = 0
for x in range(2*center-1):
    current = arr[0][0]
    # horizontal movement
    if (arr[i+1][j] > arr[i][j+1] and i <= center+1):
        move = arr[i+1][j]
        top_left.append(move)
        i += 1
    # vertical movement
    elif (j <= center+1):
        move = arr[i][j+1]
        top_left.append(move)
        j += 1

    # ending criteria
    #if (i == center and j == center - 1): break
    #if (j == center and i == center - 1): break
    # I don't think ending criteria is necessary since the loop takes care of it already
print(top_left)

# approach with the sum in a matrix
matrix = [[0 for x in range(center+1)] for y in range(center+1)] # generates a zero matrix
tl_m = [row[:] for row in matrix] # this is the way to go to copy a matrix
# simple = will be taken as a pointer, not as a copy

def compare(up,left):
    if (up == 'null'):
        if (left == 'null' and up == 'null'): return 0
        return left
    if (left == 'null'):
        if (left == 'null' and up == 'null'): return 0
        return up
    if (left == 'null' and up == 'null'): return 0
    if (up > left): return up
    else: return left

def max_matrix(temp_tlm):
    for i in range(len(temp_tlm)):
        for j in range(len(temp_tlm)):
            max_val = -999
            if (temp_tlm[i][j] > max_val): max_val = temp_tlm[i][j]
    return max_val

for i in range(center+1):
    for j in range(center+1):
        up = tl_m[i-1][j]
        left = tl_m[i][j-1]
        if (i-1 < 0):
            up = 'null'
        if (j-1 < 0):
            left = 'null'
        tl_m[i][j] = arr[i][j] + compare(up, left)

temp_tlm = [row[:] for row in tl_m]
temp_tlm[0][0] = -999
temp_tlm[len(temp_tlm)-1][len(temp_tlm)-1] = -999
max([x for x in z]) # list comprehension to obbtain the maximum value


# exception handling
try:
    gotdata = matrix[3][3]
    gd = matrix[4][4]
except IndexError:
    gotdata = 'null'
    gd = 1


def findNumber(arr, k):
    # Write your code
    ind = 0
    for i in range(len(arr)):
        if (k == arr[i]):
            ind = 1
            break
    if(ind == 0):
        print("NO")
    elif(ind == 1):
        print("YES")








