Exercise:
Write a function 'average(nlis)' that uses a 'for' loop and 'range()' to sum up 
the numbers in nlis and divide by the length of nlis. Just to be sure that you 
have used all the numbers in nlis, print each one in your 'for' loop and print 
the length of the list. Do not use the variable numlis in your function! If you 
change to a different list will it work? For numlis, the output should look 
like:

65 44 3 56 48 74 7 97 95 42 
the average is 53.1
"""

numlis = [65, 44, 3, 56, 48, 74, 7, 97, 95, 42]  # test on this list
numlis2 = [4,6,8,12,2,7,19]     # test on a second list to be sure

def average(nlis):
    pass  # delete this and enter your code starting here
    sum=0
    for i in nlis:
        sum = sum + i
        avg =sum/len(nlis)
        print(i,end=" ")
    print()
    print("the average is",avg)
        
    
    average(numlis)