Exercise:
Take the following list, nlis, and compute its average. That is, write
a function 'average(numlis)' that uses a 'for' loop to sum up the numbers
in numlis and divide by the length of numlis. Just to be sure that you
got all the numbers in numlis, print each one in your 'for' loop and 
print the length of the the list. When using a loop, one always needs to
be careful that it loops as often as is expected. In this case also print out
the number of items in the list.
Caution: Do NOT use the variable nlis in your function. This function should
work on any list of numbers. Just to be sure make sure that your function
(without any changes) works on rlis as well as nlis. 
"""

nlis = [2,4,8,105,210,-3,47,8,33,1]  # average should by 41.5
rlis = [3.14, 7.26, -4.76, 0, 8.24, 9.1, -100.7, 4] # average is -9.215

# some tests for your function. Be sure your function works for these


average(nlis)
average(rlis)

"""
Solution:
"""

def average(numlis):
    sum=0
    total=0
    for i in numlis:
        sum = sum + i
        
    total= sum/len(numlis)
    print(total)