lis = ["a","b","c","d","e","f"]

["1"]
Out[2]: ['1']

["dog"]
Out[3]: ['dog']

[2,-3,3.21]
Out[4]: [2, -3, 3.21]

lis = ["a","b","c","d","e","f"]

lis[2:4]
Out[9]: ['c', 'd']

lis[3:]
Out[10]: ['d', 'e', 'f']

lis[2:4:]
Out[11]: ['c', 'd']

lis[:3]
Out[12]: ['a', 'b', 'c']

lis
Out[13]: ['a', 'b', 'c', 'd', 'e', 'f']




lis.append("g")

lis
Out[16]: ['a', 'b', 'c', 'd', 'e', 'f', 'g']

"x" in lis
Out[17]: False

"b" in lis
Out[18]: True