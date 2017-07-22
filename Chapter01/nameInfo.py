def name():
    """ Input first and last name, combine to one string and print 
        Also, input the city and state and print."""

    fname = input("Enter your first name: ")
    lname = input("Enter your last name: ")
    fullname = fname + " " + lname
    cname = input("Enter the city you live in:")
    stname = input("Enter the state you live in:")
    print("Your name is:", fullname)
    print("You live in:",cname)
    
    print("Your state is:",stname)