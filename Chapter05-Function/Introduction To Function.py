import math
temp= max("Hello world")
print(temp)

output:
w

---------------------------------------------

import math

temp= min("Hello world")
print(temp)
output:
' '//space will print

---------------------------------------------

import math

temp= len("Hello world")
print(temp)

output:
11
---------------------------------------------

import math

temp=int ('32')
print(temp)

output:
32

---------------------------------------------

import math

temp=int ('Hello')
print(temp)

output:
 temp=int ('Hello')
ValueError: invalid literal for int() with base 10: 'Hello'

---------------------------------------------

import math

temp=int (3.99999)
print(temp)

output:
3

---------------------------------------------

import math

temp=float(33)
print(temp)

output:
33.0

---------------------------------------------

import math

temp=str(33)
print(temp)

output:
'33'

---------------------------------------------
import random

for i in range(10):
    x =random.random()
    print(x)

output:

0.765644097834104
0.031797461422213735
0.18068290968219847
0.5137724778026692
0.5324625895233822
0.3900031995935921
0.45810619552929677
0.7075454151248521
0.6815551647454572
0.061430015121717196

---------------------------------------------

The random function is only one of many functions which handle random numbers.
The function randint takes parameters low and high and returns an integer between low and high (including both).

import random
x =random.randint(5,10)
print(x)

output:
6

---------------------------------------------

import random
t = [1, 2, 3]
x =random.choice(t)
print(x)

output:
2

---------------------------------------------

import math

degree = 45
radians = degree/360.0*2*math.pi
x=math.sin(radians)
print(x)

output:
0.7071067811865475

---------------------------------------------
import math

temp=math.sqrt(2)/2

print(temp)

output:
0.707106781187


---------------------------------------------
import math

def addtwo(a,b):
    added = a + b
    return added
x = addtwo(3,6)
print(x)

output:
9

---------------------------------------------
import math


x = pow(2,9)
print(x)

output:
512

---------------------------------------------
import math


x = abs(-7)
print(x)

output:
7
---------------------------------------------

