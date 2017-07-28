fruit='banana'
letter = fruit[0]
print(letter)

output:
b
-----------------------------------------
fruit='banana'
last=len(fruit)
print(last)

output:
6
------------------------------------------
fruit='banana'
lenth=len(fruit)
last= fruit[lenth]
print(last)

output:
last= fruit[lenth]
IndexError: string index out of range

The reason for the IndexError is that there is no letter in 'banana' with the index 6.
 Since we started counting at zero, the six letters are numbered 0 to 5. 
-----------------------------------------

fruit='banana'
lenth=len(fruit)
last= fruit[lenth-1]
print(last)

output:
a
-----------------------------------------
fruit = 'banana'
index =0
while index <len(fruit):
    letter = fruit[index]
    print(letter)

    index = index +1

output:
b
a
n
a
n
a
-----------------------------------------
fruit = 'banana'
for char in fruit:
    print(char)
    
output:
b
a
n
a
n
a
------------------------------------------
String slices

s = 'Monty python'
print(s[0:5])

output:
Monty
-------------------------------------------
s = 'Monty python'
print(s[6:13])

output:
python
--------------------------------------------
greeting ='Hello, world'
greeting[0] ='j'
print(greeting[0])

output:
  greeting[0] ='j'
TypeError: 'str' object does not support item assignment
----------------------------------------------
greeting ='Hello, world'
new_greeting ='j' + greeting[0:]
print(new_greeting)

output:
jHello, world
---------------------------------------------
greeting ='Hello, world'
new_greeting ='j' + greeting[1:]
print(new_greeting)

output:
jello, world

----------------------------------------------
def check(word):
    if word < 'banana':
        print(word+" come after")
    elif word > 'banana':
        print(word+ "come after")
    elif word=='banana':
        print(word)
    else:
        print("All right bananas")
check("banana")

output:
banana
-----------------------------------------------
def check(word):
    if word == 'banana':
     new_word = word.upper()
    print(new_word)

check("banana")

output:
BANANA
------------------------------------------------
def check(word):
    if word == 'banana':
     new_word = word.find('a')
    print(new_word)

check("banana")

output:
1
------------------------------------------------
