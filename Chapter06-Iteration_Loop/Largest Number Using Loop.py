import math

largest = None
for item in [34,567,1,0]:
    if largest is None or item >largest:
        largest = item
    print("Loop:",item,largest)
print("Largest:",largest)

output:
Loop: 34 34
Loop: 567 567
Loop: 1 567
Loop: 0 567
Largest: 567
