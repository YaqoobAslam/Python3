5==5
Out[11]: True

5==6
Out[12]: False

type(True)
Out[13]: bool

type(False)
Out[14]: bool
//----------------------------------------------------
      x != y               # x is not equal to y
      x > y                # x is greater than y
      x < y                # x is less than y
      x >= y               # x is greater than or equal to y
      x <= y               # x is less than or equal to y
      x is y               # x is the same as y
      x is not y           # x is not the same as y
//---------------------------------------------------

def fun():
    choice=input("choice:")
    if choice=='a':
        print("bad guess")
    elif choice=='b':
        print("Good guess")
    elif choice=='c':
        print("close,but not correct")


fun()

output:
choice:a
bad guess

//---------------------------------------------------

def fun():
    inp = input("Enter Fahrenheit Temperature:")
    try:
        fahr = float(inp)
        cel = (fahr - 32.0) * 5.0 / 9.0
        print(cel)

    except:

        print ("Please enter a number")


fun()

output:
Enter Fahrenheit Temperature:45
7.222222222222222

//---------------------------------------------------
def fun(x):

    if x % 2 == 0:
        print( x, "is even")

    else:
        print( x, "is odd")


fun(9)
output:

9 is odd
//---------------------------------------------------

def fun(x,y):
    if x == y:
        print(x, "and", y, "are equal")

    else:
        if x < y:
            print(x, "is less than", y)

        else:
            print(x, "is greater than", y)



fun(9,8)
output:
9 is greater than 8
//---------------------------------------------------
def print_square_root(x):
    if x <= 0:
        print ("Positive numbers only, please.")
        return

    result = x**0.5
    print ("The square root of", x, "is", result)

print_square_root(8)

output:
The square root of 8 is 2.8284271247461903