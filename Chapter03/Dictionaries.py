A dictionary is like a list, but more general.
 In a list, the positions (a.k.a. indices) have to be integers;
 in a dictionary the indices can be (almost) any type.

The function dict creates a new dictionary with no items. 
Because dict is the name of a built-in function,
 you should avoid using it as a variable name.

eng2sp = dict()
print(eng2sp)

output:
{}

The squiggly-brackets, {}, represent an empty dictionary......
--------------------------------------------------------------
Strings, lists, and tuples—are sequence types, which use integers as indices to access the values.

Dictionary operations
The del statement removes a key-value pair from a dictionary. 
For example, the following dictionary contains the names of various fruits and the number of each fruit in stock: 

inventory = {'apples': 430, 'bananas': 312, 'oranges': 525, 'pears': 217}
print(inventory)


-------------------------------------------------------------
inventory = {'apples': 430, 'bananas': 312, 'oranges': 525, 'pears': 217}
print(inventory)
del inventory['pears']
print(inventory)

output:
{'apples': 430, 'bananas': 312, 'oranges': 525, 'pears': 217}
{'apples': 430, 'bananas': 312, 'oranges': 525}

-------------------------------------------------------------

inventory = {'apples': 430, 'bananas': 312, 'oranges': 525, 'pears': 217}
print(inventory)
inventory['pears']=0
print(inventory)

output:
{'apples': 430, 'bananas': 312, 'oranges': 525, 'pears': 217}
{'apples': 430, 'bananas': 312, 'oranges': 525, 'pears': 0}

-------------------------------------------------------------

inventory = {'apples': 430, 'bananas': 312, 'oranges': 525, 'pears': 217}
print(inventory.keys())
print(inventory.values())

output:
dict_keys(['apples', 'bananas', 'oranges', 'pears'])
dict_values([430, 312, 525, 217])

-------------------------------------------------------------

inventory = {'apples': 430, 'bananas': 312, 'oranges': 525, 'pears': 217}
print(inventory.items())

output:
dict_items([('apples', 430), ('bananas', 312), ('oranges', 525), ('pears', 217)])

-------------------------------------------------------------

inventory = {'apples': 430, 'bananas': 312, 'oranges': 525, 'pears': 217}
alias = inventory
copy = inventory.copy()
print(copy)


