def fahrenheit_to_celsius3():
    """ MORE IMPROVED. Does even more checking of input before using it. 
    Input from keyboard, which is always a string and must often be
    converted to an int or float. 
    Converts Fahrenheit temp to Celsius.
    Uses if to check whether input is a number and then uses .isdigit() method 
    of strings to check whether input is made of of digits. 
    """
        
    temp_str = input("Enter a Fahrentheit temperature: ")
    if temp_str:
        if temp_str.isdigit():  
            temp = int(temp_str)
            newTemp = 5*(temp-32)/9
            print("The Fahrenheit temperature",temp,"is equivalent to ",end='')
            print(newTemp,"degrees Celsius")
        else:
            print("You must enter a number. Bye")