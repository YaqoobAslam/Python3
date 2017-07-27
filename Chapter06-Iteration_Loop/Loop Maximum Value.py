import math

smallest = None
print("Before:",smallest)
for item in [3,45,67,8,15]:
    if smallest is None or item <smallest:
        smallest = item
    print("Loop:",item,smallest)
print("Smallest:",smallest)

output:

Before: None
Loop: 3 3
Loop: 45 3
Loop: 67 3
Loop: 8 3
Loop: 15 3
Smallest: 3