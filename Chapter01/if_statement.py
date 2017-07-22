def if_statement():
    """ Three slightly difference versions of if: if, if-else, if-elif-else"""
    x = 5
    y = 0
    z = 0
    if x > 0:
        print("x is positive")
        
    if y > 0:
        print("y is positive")
    else:
        print("y is not positive")
        
    # elif can be repeated as often as necessary    
    if z > 0:
        print("z is positive")
    elif z < 0:
        print("z is negative")
    else:
        print("z must be 0")