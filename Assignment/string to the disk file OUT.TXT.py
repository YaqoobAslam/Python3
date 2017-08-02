Write a  program, which initializes a string variable to the content 
"Time is a great teacher but unfortunately it kills all its pupils. Berlioz"
and outputs the string to the disk file OUT.TXT. 
you have to include all the header files if required. solution



fopen = open('OUT.TXT','w')
line ='Time is a great teacher but unfortunately it kills all its pupils. Berlioz'
fopen.write(line)

fopen.close()
