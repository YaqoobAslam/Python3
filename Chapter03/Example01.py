
def append_if_even(x,lst=None):
    if lst is None:
        lst=[]
    if x%2==0:
        lst.append(x)
        return lst



x=10    
result =append_if_even(x)
print(result)