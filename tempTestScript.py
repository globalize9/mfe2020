# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# Ask user for an input
print("Input a value here: ")
# n = int(input().strip())
n = 8;
print("Hello World!", 2+3, n);

if (1 <= n <= 100):
    if (n%2 == 1):
        print("Weird")
    if (n%2 == 0):
        if (2 <= n <= 5):
            print("Not Weird")
        elif (6 <= n <= 20):
            print("Weird")
        elif( n > 20):
            print("Not Weird")

if __name__ == '__main__':
#    a = int(input())
#    b = int(input())
    a = 3;
    b = 5;
    if (1 <= a <= 1e10 and 1 <= b <= 1e10):
        print("Sum is:", a+b);
        print("a-b is:", a-b);
        print("a*b is:", a*b);

    n = 5
    for i in list(range(0,n)):
    # remember that range goes from 0 to n-1
        print(i**2)
    for x in "banana":
        print(x)


def is_leap(year):
# functio test
    leap = False

    # Write your logic here
    if (1900 <= year <= 1e5):
        if(year % 4 == 0):
            leap = True
            if (year % 100 == 0):
                leap = False
                if (year % 400 == 0):
                    leap = True
    return leap

year = 1992
print(year, "is a leap year:", is_leap(year))

i = 1
n = 10
listZ = list(range(1,n+1))
for i in listZ:
    print(listZ[i-1], end ="")
# code above concates the numbers together
# remember python uses 0 indexing AND the end of the last number in the range argument does NOT show up


from random import randint
import numpy as np

from collections import Counter
myList = [1,1,2,3,4,5,3,2,3,4,2,1,2,3]
Counter(myList)

# x = int(input("You can specify entry here: "))
# takes x as an input and converts it to int
# can also use float
y = int(3)
x = int(2)
z = int(9)
n = int(2)

"""
for i in range( x + 1):
    for j in range( y + 1):
        if ( ( i + j ) != n ):
            print(i, j)
"""

import random
print("\n\n\nNEW SECTION***DOUBLE DOWN TEST")

capital = 1000

def gamble(capital):
    "The initial capital is ${0}, annd...".format(capital)
    bet = 1

    for i in range(1,10):
        chance = randint(1,100) % 2 # this determines the probability of winning or losing
        print("Round ", i)
        print("\nChance is: \n", chance)
        if (chance == 0):
            capital = capital - bet
        else:
            bet = bet * 2
            capital = capital + bet
            print("Your total capital is: $", capital)
            break
        bet = bet * 2

### end gamble fn
### This is why Casino has limits to upper range of betting


for i in range(3):
    gamble(capital)

words = {'apple': 'red','lemon': 'yellow'}

def Reverse(number:int) -> int:
    # Reverse an integer
    reverse = 0
    if (number > 0):
        while (number > 0):
            reminder = number % 10
            reverse = (reverse*10) + reminder
            number = number // 10 # divides and returns the integer value of a quotient

        "Reverse of {0} is {1}".format(float(number), reverse)
        return reverse

    elif (number < 0):
        number = abs(number)
        return -Reverse(number)
    # in this code...number is in fact manipulated

number = int(41250)
Reverse(number)

# 32 bits signed integers
if (number < 2**31 - 1 and number > -2**31):
    print("Integer is a 32bit signed")
else:
    print("Integer is NOT a 32bit signed")

def list2int(list):
    intc = str(list[0])
    length = len(list)
    for i in range(1,length):
        intc += str(list[i])
    return int(intc)

# List apprehension
'''x = int (input())
y = int (input())
n = int (input()) '''

x = 3
y = 2
z = 5
n = 4

# when using range, the last argument is the stopping criteria
# which does NOT get computed
list_xyz = []
list_xyz_ext = []
for i in range(x + 1):
    for j in range(y + 1):
        for k in range(z + 1):
            if (( i + j + k) != n ):
                temp = [i, j, k]
                list_xyz.append(temp)
                list_xyz_ext.extend(temp)
print(list_xyz)
# for evenly spaced out increments, use numpy library
import numpy as np
zz = np.linspace(0,10,11) # generates 0 to 1, 11 of the values


n = 8
ru = [None] * n # define a list of size n
# runner_up fn to sort the list
print("Input array separated by space:")
arr = list(map(int, input().split()))
arr = np.array([1,3,4,1,3,-5,3,5])
arr = np.array([6,6,6,6,6,6,6,5])
arr = list(arr)

# to check to see if everything in a list is greater than x
def greatereq (arr, x):
    counter = 0
    for i in arr:
        if i >= x:
            counter += 1

    if (counter == len(arr)):
        return (1)
    else:
        return (0)

def lessereq (arr, x):
    counter = 0
    for i in arr:
        if i <= x:
            counter += 1

    if (counter == len(arr)):
        return (1)
    else:
        return (0)


if (n>=2 and n<= 10 and greatereq(arr,-100) and lessereq(arr,100)):
    for i in range(len(arr)):
        ru[i] = arr[i]

    ru.sort(reverse = True)
    for i in range(len(ru)):
        if (max(ru) != ru[i]):
            print(ru[i])
            break



# intersetion of A and B set of numbers
nn = int(input())
print("Input number of students separated by space:")
n = list(map(int, input().split()))
bb = int(input())
b = list(map(int, input().split()))
#if ((len(n) + len(b)) > 0 and ((len(n) + len(b)) < 1000 )):
# the if statement only works if both n and b are independent
temp_nb = (set(n).intersection(set(b)))
print(len(temp_nb))
print(len(n.difference(b))) # the opposite of intersection

z = set(map(str, input().split()))
b = set(map(str, input().split()))
z.intersection(b)

import calendar
print("Input calendar date in MM DD YYYY:")
calendar_in = list(map(int, input().split()))
cal_int = int(''.join(map(str,calendar_in)))
print(calendar.day_name[calendar.weekday(calendar_in[2],calendar_in[0],calendar_in[1])])


import datetime as dt
time_in = "Sun 10 May 2015 13:54:36 -0700"
time_in2 = "Sun 10 May 2015 13:54:36 -0000"

t_arr = ["Sun 10 May 2015 13:54:36 -0700",
"Sun 10 May 2015 13:54:36 -0000",
"Sat 02 May 2015 19:54:36 +0530",
"Fri 01 May 2015 13:54:36 -0000"]

t1 = dt.datetime.strptime(t_arr[0], '%a %d %B %Y %H:%M:%S %z')
t2 = dt.datetime.strptime(t_arr[1], '%a %d %B %Y %H:%M:%S %z')

int((t1-t2).total_seconds())



# array in python with building across dimensions
import numpy
dim_arr = list(map(int, input().split())) #2nd value is column
arr = numpy.zeros((dim_arr), dtype = int) # initialize an array of zeros

# this is a column input...you could use row input
for j in range(dim_arr[1]):
    "Input {0} column data:".format(j)
    arr[:,j] = list(map(int,input().split()))


print(arr)
print(numpy.transpose(arr).flatten())


# extract the numerical portion of an input
N = int(input()) # number of commands to be executed
list = []

for i in range(N):
    str = input()
    digits = [int(j) for j in str.split() if j.isdigit()]
    cmd = str.split()[0]
    if (cmd == "insert"):
        list.insert(digits[0], digits[1])
    elif (cmd == "print"):
        print(list)
    elif (cmd == "remove"):
        list.remove(digits[0])
    elif (cmd == "append"):
        list.append(digits[0])
    elif (cmd == "sort"):
        list.sort()
    elif (cmd == "pop"):
        list.pop()
    elif (cmd == "reverse"):
        list.reverse()



















