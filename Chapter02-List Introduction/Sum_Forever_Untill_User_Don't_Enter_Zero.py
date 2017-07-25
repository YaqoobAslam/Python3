"""
Example: Add numbers until you get a blank one. This initializes a variable
sum_ and adds to it each time through the loop. Afterwards sum_ is used in a
print statement.
"""
def add_up():
    sum_ = 0
    while True:             # will loop forever
        num = int(input("Enter a number, input 0 to quit: "))
        if num == 0:
            break           # breaks out of while loop
        sum_ = sum_ + num
    print(sum_)
