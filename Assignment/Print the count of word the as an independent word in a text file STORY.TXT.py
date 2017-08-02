Write a function in  to print the count of word the as an independent word in a text file STORY.TXT.
for example, if the content of the file STORY.TXT is
There was a monkey in the zoo. The monkey was very naughty.

def func():
 word=0
num_words = 0
fread = open('STORY.TXT','r')
for line in fread:
    words = line.split()
    num_words += len(words)
    print( words)
    print("Total words are:",num_words)



func()

output:

['There', 'was', 'a', 'monkey', 'in', 'the', 'zoo.', 'The', 'monkey', 'was', 'very', 'naughty']
Total words are: 12

