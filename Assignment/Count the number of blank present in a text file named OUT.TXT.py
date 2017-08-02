Write a function to count the number of blank present in a text file named "OUT.TXT". solution


spaces=0
fread = open('OUT.TXT','r')
for line in fread:
    spaces += line.count(' ')
    print("Total space is:",spaces)

output:
Total space is: 12