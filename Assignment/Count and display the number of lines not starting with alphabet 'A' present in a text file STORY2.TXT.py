Write a function in  to count and display the number of lines not starting with alphabet 'A' present in a text file "STORY.TXT".
Example:
If the file "STORY.TXT" contains the following lines,
The rose is red.
A girl is playing there.
There is a playground.
An aeroplane is in the sky.
Numbers are not allowed in the password.


def func():
 Count = 0
 fread = open('STORY2.TXT','r')
 for line in fread:
    lines = line
    if lines.startswith('A'):
        continue
    Count +=1
    print(lines)

 print("Number of lines is:",Count)

func()


output:


The rose is red.

A girl is playing there.

There is a playground.

An aeroplane is in the sky.

Numbers are not allowed in the password.

Number of lines is: 5

----------------------------------------

The rose is red.

There is a playground.

Numbers are not allowed in the password.
Number of lines is: 3