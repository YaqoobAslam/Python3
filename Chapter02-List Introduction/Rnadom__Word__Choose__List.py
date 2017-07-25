"""The following example builds a sentence using various parts of speech.
It randomly chooses words from a list by using random.choice(), a function
or method imported from a library called random. We have used a method of the
string data type to capitalize the first letter of the sentence.
"""

import random

verbs=["goes","cooks","shoots","faints","chews","screams"]
nouns=["bear","lion","mother","baby","sister","car","bicycle","book"]
adverbs=["handily","sweetly","sourly","gingerly","forcefully","meekly"]
articles=["a","the","that","this"]
def sentence():
    article = random.choice(articles)
    noun = random.choice(nouns)
    verb = random.choice(verbs)
    adverb =random.choice(adverbs)
    our_sentence = article+ " " +noun+ " " +verb+ " "+adverb+"."
    our_sentence = our_sentence.capitalize()
    print(our_sentence)

    
""" Function calling """
sentence()
