"""
Exercise:
Write a function diner_waitress() that asks for you order. First start an empty
list, call it order. Then use a while loop and an input() statement to gather
the order. Continue in the while loop until the customer says "that's all". 
Onne way to end the loop is to use 'break' to break out of the loop when 
"that's all" is entered. 
Recall that you can add to a list by using the list's .append() method; suppose
that your list is called order. To create an empty list you can use
order = []. You are going to have to input one food at a time and append it
to the order list.
Then print out the order. Here is my run:

diner_waitress()
Hello, I'll be your waitress. What will you have?

menu item: eggs

menu item: bacon

menu item: toast

menu item: jelly

menu item: that's all
You've ordered:
['eggs', 'bacon', 'toast', 'jelly']

"""


def diner_waitress():
    order_list =[]
    while True:
        item_list = input("Hello, I'll be your waitress. What will you have?")
        if item_list == "that's all":
            break
        order_list.append(item_list)
    print("menu item:",order_list)

diner_waitress()

output:
Hello, I'll be your waitress. What will you have?papsi
Hello, I'll be your waitress. What will you have?mango
Hello, I'll be your waitress. What will you have?jelly
Hello, I'll be your waitress. What will you have?that's all
menu item: ['papsi', 'mango', 'jelly']

