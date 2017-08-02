Write a function to count number of words in a text file named "OUT.TXT". solution


def func():
 word=0
num_words = 0
fread = open('OUT.TXT','r')
for line in fread:
    words = line.split()
    num_words += len(words)
    print("Total words are:",num_words)



func()

output:
Total words are: 13