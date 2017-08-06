
Quadratic equations are equations of the form 2 ax + bx + c = 0 where a ? 0
describe parabolas. The roots of such equations are derived from the formula
?It is possible to use other encodings. See the Python Tutorial’s “Source Code Encoding” topic.
From the Library of STEPHEN EISEMAN
ptg
Examples 95
x = -b±v 2
b -4ac
2a . The 2
b - 4ac part of the formula is called the discriminant—if it
is positive there are two real roots, if it is zero there is one real root, and if it is
negative there are two complex roots. We will write a program that accepts the
a, b, and c factors from the user (with the b and c factors allowed to be 0), and
then calculates and outputs the root or roots.?
First we will look at a sample run, and then we will review the code.
quadratic.py
ax² + bx + c = 0
enter a: 2.5
enter b: 0
enter c: -7.25
2.5x² + 0.0x + -7.25 = 0 ? x = 1.70293863659 or x = -1.70293863659
With factors 1.5, -3, and 6, the output (with some digits trimmed) is:
1.5x² + -3.0x + 6.0 = 0 ? x = (1+1.7320508j) or x = (1-1.7320508j)
The output isn’t quite as tidy as we’d like—for example, rather than + -3.0x
it would be nicer to have - 3.0x, and we would prefer not to have any 0 factors
shown at all. You will get the chance to fix these problems in the exercises.
Now we will turn to the code, which begins with three imports:
import cmath
import math
import sys
We need both the float and the complex math libraries since the square root
functions for real and complex numbers are different, and we need sys for
sys.float_info.epsilon which we need to compare floating-point numbers
with 0.
We also need a function that can get a floating-point number from the user:
def get_float(msg, allow_zero):
x = None
while x is None:
try:
x = float(input(msg))
if not allow_zero and abs(x) < sys.float_info.epsilon:
print("zero is not allowed")
x = None
? Since the Windows console has poor UTF-8 support, there are problems with a couple of the
characters (² and ?) that quadratic.py uses. We have provided quadratic_uni.py which displays the
correct symbols on Linux and Mac OS X, and alternatives (^2 and ->) on Windows.
From the Library of STEPHEN EISEMAN
ptg
96 Chapter 2. Data Types
except ValueError as err:
print(err)
return x
This function will loop until the user enters a valid floating-point number (such
as 0.5, -9, 21, 4.92), and will accept 0 only if allow_zero is True.
Once the get_float() function is defined, the rest of the code is executed. We’ll
look at it in three parts, starting with the user interaction:
print("ax\N{SUPERSCRIPT TWO} + bx + c = 0")
a = get_float("enter a: ", False)
b = get_float("enter b: ", True)
c = get_float("enter c: ", True)
Thanks to the get_float() function, getting the a, b, and c factors is simple. The
Boolean second argument says whether 0 is acceptable.
x1 = None
x2 = None
discriminant = (b ** 2) - (4 * a * c)
if discriminant == 0:
x1 = -(b / (2 * a))
else:
if discriminant > 0:
root = math.sqrt(discriminant)
else: # discriminant < 0
root = cmath.sqrt(discriminant)
x1 = (-b + root) / (2 * a)
x2 = (-b - root) / (2 * a)
The code looks a bit different to the formula because we begin by calculating
the discriminant. If the discriminant is 0, we know that we have one real
solution and so we calculate it directly. Otherwise, we take the real or complex
square root of the discriminant and calculate the two roots.
equation = ("{0}x\N{SUPERSCRIPT TWO} + {1}x + {2} = 0"
" \N{RIGHTWARDS ARROW} x = {3}").format(a, b, c, x1)
if x2 is not None:
equation += " or x = {0}".format(x2)
print(equation)
We haven’t done any fancy formatting since Python’s defaults for floating-point
numbers are fine for this example, but we have used Unicode character names
for a couple of special characters.
From the Library of STEPHEN EISEMAN
ptg
Examples 97
Us- A more robust alternative to using positional arguments with their

index positions
as field names, is to use the dictionary returned by locals(), a technique
we saw earlier in the chapter.
3.1
equation = ("{a}x\N{SUPERSCRIPT TWO} + {b}x + {c} = 0"
" \N{RIGHTWARDS ARROW} x = {x1}").format(**locals())
And if we are using Python 3.1, we could omit the field names and leave Python
to populate the fields using the positional arguments passed to str.format().
equation = ("{}x\N{SUPERSCRIPT TWO} + {}x + {} = 0"
" \N{RIGHTWARDS ARROW} x = {}").format(a, b, c, x1)
This is convenient, but not as robust as using named parameters, nor as
versatile if we needed to use format specifications. Nonetheless, for many
simple cases this syntax is both easy and useful.



import  cmath
import  math
import  sys

def get_float(msg,allow_zero):
    x =None
    while x is None:
        try:
            x=float(input(msg))
            if not allow_zero and abs(x) <sys.float_info.epsilon:
                print("zero is not allowed")
                x=None
        except ValueError as err:
            print(err)
    return x


print("ax\N{SUPERSCRIPT TWO} + bx + c =0")
a = get_float("enter a:",False)
b = get_float("enter b:",True)
c = get_float("enter c:",True)

x1 = None
x2 = None

discriminant = (b**2) - (4*a*c)
if discriminant == 0:
    x1 =-(b/(2*a))
else:
    if discriminant > 0:
        root = math.sqrt(discriminant)
    else:#discriminant < 0 ho to ya case laga ga
        root = cmath.sqrt(discriminant)
    x1 = (-b + root)/(2 * a)
    x2 = (-b -root)/(2 * a)

equation = ("{0}x\N{SUPERSCRIPT TWO} + {1}x +{2}=0" " \N{RIGHTWARDS ARROW} x = {3}".format(a, b,c, x1))

if x2 is not None:
    equation += "or x={0}".format(x2)
print(equation)

output:
ax² + bx + c =0
enter a:2
enter b:3
enter c:6
2.0x² + 3.0x +6.0=0 ? x = (-0.75+1.5612494995995996j)or x=(-0.75-1.5612494995995996j)
--------------------------------------------------------------------------------------------------------------------------------------------

1. Modify the print_unicode.py program so that the user can enter several
separate words on the command line, and print rows only where the
Unicode character name contains all the words the user has specified.
This means that we can type commands like this:
print_unicode_ans.py greek symbol
One way of doing this is to replace the word variable (which held 0, None,
or a string), with a words list. Don’t forget to update the usage information
as well as the code. The changes involve adding less than ten lines
of code, and changing less than ten more. A solution is provided in file
print_unicode_ans.py. (Windows and cross-platform users should modify
print_unicode_uni.py; a solution is provided in print_unicode_uni_ans.py.)

import cmath
import math
import sys


def get_float(msg, allow_zero):
    x = None
    while x is None:
        try:
            x = float(input(msg))
            if not allow_zero and abs(x) < sys.float_info.epsilon:
                print("zero is not allowed")
                x = None
        except ValueError as err:
            print(err)
    return x


print("ax\N{SUPERSCRIPT TWO} + bx + c = 0")
a = get_float("enter a: ", False)
b = get_float("enter b: ", True)
c = get_float("enter c: ", True)

x1 = None
x2 = None
discriminant = (b ** 2) - (4 * a * c)
if discriminant == 0:
    x1 = -(b / (2 * a))
else:
    if discriminant > 0:
        root = math.sqrt(discriminant)
    else: # discriminant < 0
        root = cmath.sqrt(discriminant)
    x1 = (-b + root) / (2 * a)
    x2 = (-b - root) / (2 * a)

equation = "{0}x\N{SUPERSCRIPT TWO} ".format(a)
if b != 0:
    if b < 0:
        equation += "- {0}x ".format(abs(b))
    else:
        equation += "+ {0}x ".format(b)
if c != 0:
    if c < 0:
        equation += "- {0} ".format(abs(c))
    else:
        equation += "+ {0} ".format(c)
equation += "= 0 \N{RIGHTWARDS ARROW} x = {0}".format(x1)
if x2 is not None:
    equation += " or x = {0}".format(x2)
print(equation)

output:
ax² + bx + c = 0
enter a: -2
enter b: -10
enter c: 9
-2.0x² - 10.0x + 9.0 = 0 ? x = -5.778719262151 or x = 0.7787192621510002
--------------------------------------------------------------------------------------------------------------------------------------------

2. Modify quadratic.py so that 0.0 factors are not output, and so that negative
factors are output as - n rather than as + -n. This involves replacing the
last five lines with about fifteen lines. A solution is provided in quadratic_ans.py.
(Windows and cross-platform users should modify quadratic_uni.py;
a solution is provided in quadratic_uni_ans.py.)

import cmath
import math
import sys


SQUARED = "\N{SUPERSCRIPT TWO}"
ARROW = "\N{RIGHTWARDS ARROW}"
if not sys.platform.startswith("linux"):
    SQUARED = "^2"
    ARROW = "->"


def get_float(msg, allow_zero):
    x = None
    while x is None:
        try:
            x = float(input(msg))
            if not allow_zero and abs(x) < sys.float_info.epsilon:
                print("zero is not allowed")
                x = None
        except ValueError as err:
            print(err)
    return x


print("ax" + SQUARED + " + bx + c = 0")
a = get_float("enter a: ", False)
b = get_float("enter b: ", True)
c = get_float("enter c: ", True)

x1 = None
x2 = None
discriminant = (b ** 2) - (4 * a * c)
if discriminant == 0:
    x1 = -(b / (2 * a))
else:
    if discriminant > 0:
        root = math.sqrt(discriminant)
    else: # discriminant < 0
        root = cmath.sqrt(discriminant)
    x1 = (-b + root) / (2 * a)
    x2 = (-b - root) / (2 * a)

equation = ("{a}x{SQUARED} + {b}x + {c} = 0 {ARROW} x = {x1}"
            .format(**locals()))
if x2 is not None:
    equation += " or x = {0}".format(x2)
print(equation)

output:
ax^2 + bx + c = 0
enter a: 12
enter b: 3
enter c: 63
12.0x^2 + 3.0x + 63.0 = 0 -> x = (-0.125+2.287875652215391j) or x = (-0.125-2.287875652215391j)
--------------------------------------------------------------------------------------------------------------------------------------------
One common requirement is to take a data set and present it using HTML. In
this subsection we will develop a program that reads a file that uses a simple
CSV (Comma Separated Value) format and outputs an HTML table containing
the file’s data. Python comes with a powerful and sophisticated module for
handling CSV and similar formats—the csv module—but here we will write
all the code by hand.
The CSV format we will support has one record per line, with each record
divided into fields by commas. Each field can be either a string or a number.
Strings must be enclosed in single or double quotes and numbers should be
unquoted unless they contain commas. Commas are allowed inside strings,
and must not be treated as field separators. We assume that the first record
contains field labels. The output we will produce is an HTML table with text
left-aligned (the default in HTML) and numbers right-aligned, with one row
per record and one cell per field.
The program must output the HTML table’s opening tag, then read each line of
data and for each one output an HTML row, and at the end output the HTML
table’s closing tag. We want the background color of the first row (which will
display the field labels) to be light green, and the background of the data rows
to alternate between white and light yellow. We must also make sure that the
special HTML characters (“&”, “<”, and “>”) are properly escaped, and we want
strings to be tidied up a bit.
Here’s a tiny piece of sample data:
"COUNTRY","2000","2001",2002,2003,2004
"ANTIGUA AND BARBUDA",0,0,0,0,0
From the Library of STEPHEN EISEMAN
ptg
98 Chapter 2. Data Types
"ARGENTINA",37,35,33,36,39
"BAHAMAS, THE",1,1,1,1,1
"BAHRAIN",5,6,6,6,6
Assuming the sample data is in the file data/co2-sample.csv, and given
the command csv2html.py < data/co2-sample.csv > co2-sample.html, the file
co2-sample.html will have contents similar to this:
<table border='1'><tr bgcolor='lightgreen'>
<td>Country</td><td align='right'>2000</td><td align='right'>2001</td>
<td align='right'>2002</td><td align='right'>2003</td>
<td align='right'>2004</td></tr>
...
<tr bgcolor='lightyellow'><td>Argentina</td>
<td align='right'>37</td><td align='right'>35</td>
<td align='right'>33</td><td align='right'>36</td>
<td align='right'>39</td></tr>
...
</table>
We’ve tidied the output slightly and omitted some lines where indicated by
ellipses. We have used a very simple version of HTML—HTML 4 transitional,
with no style sheet. Figure 2.7 shows what the output looks like in a web
browser.
Figure 2.7 A csv2html.py table in a web browser
Now that we’ve seen how the program is used and what it does, we are ready
to review the code. The program begins with the import of the sys module; we
won’t show this, or any other imports from now on, unless they are unusual
or warrant discussion. And the last statement in the program is a single
function call:
main()
Although Python does not need an entry point as some languages require, it
is quite common in Python programs to create a function called main() and to
call it to start off processing. Since no function can be called before it has been
created, we must make sure we call main() after the functions it relies on have
From the Library of STEPHEN EISEMAN
ptg
Examples 99
been defined. The order in which the functions appear in the file (i.e., the order
in which they are created) does not matter.
In the csv2html.py program, the first function we call is main() which in turn
calls print_start() and then print_line(). And print_line() calls extract_
fields() and escape_html(). The program structure we have used is shown in
Figure 2.8.
import sys
def main():
def print_start():
def print_line():
def extract_fields():
def escape_html():
def print_end():
main()
calls
calls
calls
Figure 2.8 The csv2html.py program’s structure
When Python reads a file it begins at the top. So for this example, it starts by
performing the import, then it creates the main() function, and then it creates
the other functions in the order in which they appear in the file. When Python
finally reaches the call to main() at the end of the file, all the functions that
main() will call (and all the functions that those functions will call) now exist.
Execution as we normally think of it begins where the call to main() is made.
We will look at each function in turn, starting with main().
def main():
maxwidth = 100
print_start()
count = 0
while True:
try:
line = input()
if count == 0:
color = "lightgreen"
elif count % 2:
color = "white"
else:
color = "lightyellow"
From the Library of STEPHEN EISEMAN
ptg
100 Chapter 2. Data Types
print_line(line, color, maxwidth)
count += 1
except EOFError:
break
print_end()
The maxwidth variable is used to constrain the number of characters in a
cell—if a field is bigger than this we will truncate it and signify this by adding
an ellipsis to the truncated text. We’ll look at the print_start(), print_line(),
and print_end() functions in a moment. The while loop iterates over each line
of input—this could come from the user typing at the keyboard, but we expect
it to be a redirected file. We set the color we want to use and call print_line()
to output the line as an HTML table row.
def print_start():
print("<table border='1'>")
def print_end():
print("</table>")
We could have avoided creating these two functions and simply put the relevant
print() function calls in main(). But we prefer to separate out the logic
since this is more flexible, even though it doesn’t really matter in this small
example.
def print_line(line, color, maxwidth):
print("<tr bgcolor='{0}'>".format(color))
fields = extract_fields(line)
for field in fields:
if not field:
print("<td></td>")
else:
number = field.replace(",", "")
try:
x = float(number)
print("<td align='right'>{0:d}</td>".format(round(x)))
except ValueError:
field = field.title()
field = field.replace(" And ", " and ")
if len(field) <= maxwidth:
field = escape_html(field)
else:
field = "{0} ...".format(
escape_html(field[:maxwidth]))
print("<td>{0}</td>".format(field))
print("</tr>")
From the Library of STEPHEN EISEMAN
ptg
Examples 101
We cannot use str.split(",") to split each line into fields because commas
can occur inside quoted strings. So we have farmed this work out to the
extract_fields() function. Once we have a list of the fields (as strings, with no
surrounding quotes), we iterate over them, creating a table cell for each one.
If a field is empty, we output an empty cell. If a field is quoted, it could be
a string or it could be a number that has been quoted to allow for internal
commas, for example, "1,566". To account for this, we make a copy of the field
with commas removed and try to convert the field to a float. If the conversion is
successful we output a right-aligned cell with the field rounded to the nearest
whole number and output it as an integer. If the conversion fails we output the
field as a string. In this case we use str.title() to neaten the case of the letters
and we replace the word And with and as a correction to str.title()’s effect.
If the field isn’t too long we use all of it, otherwise we truncate it to maxwidth
characters and add an ellipsis to signify the truncation, and in either case we
escape any special HTML characters the field might contain.
def extract_fields(line):
fields = []
field = ""
quote = None
for c in line:
if c in "\"'":
if quote is None: # start of quoted string
quote = c
elif quote == c: # end of quoted string
quote = None
else:
field += c # other quote inside quoted string
continue
if quote is None and c == ",": # end of a field
fields.append(field)
field = ""
else:
field += c # accumulating a field
if field:
fields.append(field) # adding the last field
return fields
This function reads the line it is given character by character, accumulating
a list of fields—each one a string without any enclosing quotes. The function
copes with fields that are unquoted, and with fields that are quoted with single
or double quotes, and correctly handles commas and quotes (single quotes in
double quoted strings, double quotes in single quoted strings).
From the Library of STEPHEN EISEMAN
ptg
102 Chapter 2. Data Types
def escape_html(text):
text = text.replace("&", "&amp;")
text = text.replace("<", "&lt;")
text = text.replace(">", "&gt;")
return text
This function straightforwardly replaces each special HTML character with
the appropriate HTML entity. We must of course replace ampersands first,
although the order doesn’t matter for the angle brackets. Python’s standard
library includes a slightly more sophisticated version of this function—you’ll
get the chance to use it in the exercises, and will see it again in Chapter 7.





import sys

def main():
    maxwidth = 100
    print_start()
    count = 0
    while True:
        try:
            line = input()
            if count == 0:
                color = "lightgreen"
            elif count % 2:
                color = "white"
            else:
                color = "lightyellow"
            print_line(line, color, maxwidth)
            count += 1
        except EOFError:
            break
    print_end()


def print_start():
    print("<table border='1'>")


def print_line(line, color, maxwidth):
    print("<tr bgcolor='{0}'>".format(color))
    fields = extract_fields(line)
    for field in fields:
        if not field:
            print("<td></td>")
        else:
            number = field.replace(",", "")
            try:
                x = float(number)
                print("<td align='right'>{0:d}</td>".format(round(x)))
            except ValueError:
                field = field.title()
                field = field.replace(" And ", " and ")
                if len(field) <= maxwidth:
                    field = escape_html(field)
                else:
                    field = "{0} ...".format(
                            escape_html(field[:maxwidth]))
                print("<td>{0}</td>".format(field))
    print("</tr>")


def extract_fields(line):
    fields = []
    field = ""
    quote = None
    for c in line:
        if c in "\"'":
            if quote is None: # start of quoted string
                quote = c
            elif quote == c:  # end of quoted string
                quote = None
            else:
                field += c    # other quote inside quoted string
            continue
        if quote is None and c == ",": # end of a field
            fields.append(field)
            field = ""
        else:
            field += c        # accumulating a field
    if field:
        fields.append(field)  # adding the last field
    return fields


def escape_html(text):
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text


def print_end():
    print("</table>")


main()


--------------------------------------------------------------------------------------------------------------------------------------------

3. Delete the escape_html() function from csv2html.py, and use the xml.sax.
saxutils.escape() function from the xml.sax.saxutils module instead. This
is easy, requiring one new line (the import), five deleted lines (the unwanted
function), and one changed line (to use xml.sax.saxutils.escape() instead
of escape_html()). A solution is provided in csv2html1_ans.py.

import sys
import xml.sax.saxutils


def main():
    maxwidth = 100
    print_start()
    count = 0
    while True:
        try:
            line = input()
            if count == 0:
                color = "lightgreen"
            elif count % 2:
                color = "white"
            else:
                color = "lightyellow"
            print_line(line, color, maxwidth)
            count += 1
        except EOFError:
            break
    print_end()


def print_start():
    print("<table border='1'>")


def print_line(line, color, maxwidth):
    print("<tr bgcolor='{0}'>".format(color))
    fields = extract_fields(line)
    for field in fields:
        if not field:
            print("<td></td>")
        else:
            number = field.replace(",", "")
            try:
                x = float(number)
                print("<td align='right'>{0:d}</td>".format(round(x)))
            except ValueError:
                field = field.title()
                field = field.replace(" And ", " and ")
                if len(field) <= maxwidth:
                    field = xml.sax.saxutils.escape(field)
                else:
                    field = "{0} ...".format(
                            xml.sax.saxutils.escape(field[:maxwidth]))
                print("<td>{0}</td>".format(field))
    print("</tr>")


def extract_fields(line):
    fields = []
    field = ""
    quote = None
    for c in line:
        if c in "\"'":
            if quote is None: # start of quoted string
                quote = c
            elif quote == c:  # end of quoted string
                quote = None
            else:
                field += c    # other quote inside quoted string
            continue
        if quote is None and c == ",": # end of a field
            fields.append(field)
            field = ""
        else:
            field += c        # accumulating a field
    if field:
        fields.append(field)  # adding the last field
    return fields


def print_end():
    print("</table>")


main()

--------------------------------------------------------------------------------------------------------------------------------------------

4. Modify csv2html.py again, this time adding a new function called process_options().
This function should be called from main() and should
return a tuple of two values: maxwidth (an int) and format (a str). When
process_options() is called it should set a default maxwidth of 100, and a
default format of “.0f ”—this will be used as the format specifier when outputting
numbers.
From the Library of STEPHEN EISEMAN
ptg
Exercises 105
If the user has typed “-h” or “--help” on the command line, a usage message
should be output and (None, None) returned. (In this case main() should
do nothing.) Otherwise, the function should read any command-line
arguments that are given and perform the appropriate assignments. For
example, setting maxwidth if “maxwidth=n” is given, and similarly setting
format if “format=s” is given. Here is a run showing the usage output:
csv2html2_ans.py -h
usage:
csv2html.py [maxwidth=int] [format=str] < infile.csv > outfile.html
maxwidth is an optional integer; if specified, it sets the maximum
number of characters that can be output for string fields,
otherwise a default of 100 characters is used.
format is the format to use for numbers; if not specified it
defaults to ".0f".
And here is a command line with both options set:
csv2html2_ans.py maxwidth=20 format=0.2f < mydata.csv > mydata.html
Don’t forget to modify print_line() to make use of the format for outputting
numbers—you’ll need to pass in an extra argument, add one line,
and modify another line. And this will slightly affect main() too. The process_options()
function should be about twenty-five lines (including about
nine for the usage message). This exercise may prove challenging for inexperienced
programmers.
Two files of test data are provided: data/co2-sample.csv and data/co2-fromfossilfuels.csv.
A solution is provided in csv2html2_ans.py. In Chapter 5
we will see how to use Python’s optparse module to simplify command-line
processing.



import sys
import xml.sax.saxutils


def main():
    maxwidth, format = process_options()
    if maxwidth is not None:
        print_start()
        count = 0
        while True:
            try:
                line = input()
                if count == 0:
                    color = "lightgreen"
                elif count % 2:
                    color = "white"
                else:
                    color = "lightyellow"
                print_line(line, color, maxwidth, format)
                count += 1
            except EOFError:
                break
        print_end()


def process_options():
    maxwidth_arg = "maxwidth="
    format_arg = "format="
    maxwidth = 100
    format = ".0f"
    for arg in sys.argv[1:]:
        if arg in ["-h", "--help"]:
            print("""\
usage:
csv2html.py [maxwidth=int] [format=str] < infile.csv > outfile.html
maxwidth is an optional integer; if specified, it sets the maximum
number of characters that can be output for string fields,
otherwise a default of {0} characters is used.
format is the format to use for numbers; if not specified it
defaults to "{1}".""".format(maxwidth, format))
            return None, None
        elif arg.startswith(maxwidth_arg):
            try:
                maxwidth = int(arg[len(maxwidth_arg):])
            except ValueError:
                pass
        elif arg.startswith(format_arg):
            format = arg[len(format_arg):]
    return maxwidth, format


def print_start():
    print("<table border='1'>")


def print_line(line, color, maxwidth, format):
    print("<tr bgcolor='{0}'>".format(color))
    numberFormat = "<td align='right'>{{0:{0}}}</td>".format(format)
    fields = extract_fields(line)
    for field in fields:
        if not field:
            print("<td></td>")
        else:
            number = field.replace(",", "")
            try:
                x = float(number)
                print(numberFormat.format(x))
            except ValueError:
                field = field.title()
                field = field.replace(" And ", " and ")
                if len(field) <= maxwidth:
                    field = xml.sax.saxutils.escape(field)
                else:
                    field = "{0} ...".format(
                            xml.sax.saxutils.escape(field[:maxwidth]))
                print("<td>{0}</td>".format(field))
    print("</tr>")


def extract_fields(line):
    fields = []
    field = ""
    quote = None
    for c in line:
        if c in "\"'":
            if quote is None:
                quote = c
            elif quote == c:
                quote = None
            else:
                field += c
            continue
        if quote is None and c == ",":
            fields.append(field)
            field = ""
        else:
            field += c
    if field:
        fields.append(field)
    return fields


def print_end():
    print("</table>")


main()
