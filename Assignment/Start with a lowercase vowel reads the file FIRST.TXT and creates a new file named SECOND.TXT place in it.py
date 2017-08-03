Assuming that a text file named FIRST.TXT contains some text written into it, write a function named vowelwords(),
that reads the file FIRST2.TXT and creates a new file named SECOND2.TXT,
to contain only those words from the file FIRST.TXT which start with a lowercase vowel (i.e., with 'a', 'e', 'i', 'o', 'u'). 


def vowelwords():

 fread  = open('FIRST2.TXT','r')

 fopen = open('SECOND2.TXT','w')
 for lines in fread:
    vowel =('a', 'e', 'i', 'o', 'u')
    if lines.startswith(vowel):

     fopen.write( lines )

vowelwords()
