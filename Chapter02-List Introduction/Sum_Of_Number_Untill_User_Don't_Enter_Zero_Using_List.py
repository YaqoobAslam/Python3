""" 
Let's write a program to build a list of the numbers. Before we initialized 
sum_ to 0. The equivalent for a list is to set it to the empty list. Adding to
the sum has its equivalent in appending to the list.
"""



def store_up():
    num_list =[]
    while True:
        nextnum = int(input("Enter a number, 0 to quit:"))
        if nextnum == 0:
            break
        num_list.append(nextnum)
    print(num_list)


store_up()

output:
Enter a number, 0 to quit:12
Enter a number, 0 to quit:63
Enter a number, 0 to quit:63
Enter a number, 0 to quit:0
[12, 63, 63]