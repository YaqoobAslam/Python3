

Write a C++ program to write number 1 to 100 in a data file NOTES.TXT. solution


fopen = open('NOTES.TXT','w')

n=1	#define n variable
while n<=100:
    line =str(n)
    fopen.write(line)

    n = n + 1

fopen.close()
