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


