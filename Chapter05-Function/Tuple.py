Tuples are immutable

t='a','b','c','d'
------------------------------------------
 t = ('a',)
 type(t)
<class 'tuple'>
------------------------------------------
t=('a')
 type(t)
<class 'str'>
------------------------------------------
tup = 2, 4, 6, 8, 10
------------------------------------------
t=(2,)
 type(t)
<class 'tuple'>
------------------------------------------
Another way to construct a tuple is the built-in function tuple. With no argument, it creates an empty tuple:

 
t = tuple()
print t

output:
()
------------------------------------------
tup =('a','b','c','d','e')
print(tup[0])

output:
a
------------------------------------------
tup =('a','b','c','d','e')
print(tup[1:3])

output:
('b', 'c')
------------------------------------------
tup = ('a', 'b', 'c', 'd', 'e')
tup[0] ='x'
print(tup)

output:
  tup[0] ='x'
NameError: name 'tup' is not defined

------------------------------------------
tup = ('a', 'b', 'c', 'd', 'e')
tup =('x',) + tup[2:]
print(tup)

output:
('x', 'c', 'd', 'e')
------------------------------------------
tup = ('a', 'b', 'c', 'd', 'e')
tup =('x',) + tup[:2]
print(tup)

output:
('x', 'a', 'b')

------------------------------------------
Comparing tuples

print((0,1,2) < (0,3,4))
True
------------------------------------------
print( (0,3,0) <(0,1,0))
False
------------------------------------------
Tuple assignment


m = ['have','fun']
x,y = m
print(y)
print(x)

output:
fun
have
------------------------------------------
m = ['have','fun']
x =m[0]
y =m[1]
print(x)
print(y)

output:
have
fun
------------------------------------------
def swap(x,y):
  return y,x

val = swap(5,9)
print(val)

output:
(9, 5)

------------------------------------------
Dictionaries and tuples

d = {'a':10, 'b':1,'c':22}
t = d.items()
print(t)

output:
dict_items([('a', 10), ('b', 1), ('c', 22)])

------------------------------------------

Multiple assignment with dictionaries

d = {'a':10, 'b':1,'c':22}

for key,val in d.items():
  print(key,val)

output:
a 10
b 1
c 22





