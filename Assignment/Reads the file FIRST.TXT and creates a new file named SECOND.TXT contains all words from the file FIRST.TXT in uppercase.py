Assuming that a text file named FIRST.TXT contains some text written into it,
write a function named copyupper()
that reads the file FIRST.TXT and creates a new file named SECOND.TXT contains all words from the file FIRST.TXT in uppercase.


def copyupper():

 fread  = open('FIRST.TXT','r')     #Read from file.

 fopen = open('SECOND.TXT','w')
 for lines in fread:                # fread as object copy into lines and write into second file.
     fopen.write(lines.upper())     #call function upper() to convert into capital letters.

copyupper()
