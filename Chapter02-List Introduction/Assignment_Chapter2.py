Imagine we are setting up a new computer system and need to generate usernames
for all of our organization’s staff. We have a plain text data file (UTF-
8 encoding) where each line represents a record and fields are colon-delimited.
Each record concerns one member of the staff and the fields are their unique
staff ID, forename, middle name (which may be an empty field), surname,
and department name. Here is an extract of a few lines from an example
data/users.txt data file:
1601:Albert:Lukas:Montgomery:Legal
3702:Albert:Lukas:Montgomery:Sales
4730:Nadelle::Landale:Warehousing
The program must read in all the data files given on the command line, and for
every line (record) must extract the fields and return the data with a suitable
username. Each username must be unique and based on the person’s name.
The output must be text sent to the console, sorted alphabetically by surname
and forename, for example:
Name ID Username
-------------------------------- ------ ---------
Landale, Nadelle................ (4730) nlandale
Montgomery, Albert L............ (1601) almontgo
Montgomery, Albert L............ (3702) almontgo1


Each record has exactly five fields, and although we could refer to them by
number, we prefer to use names to keep our code clear:
ID, FORENAME, MIDDLENAME, SURNAME, DEPARTMENT = range(5)
It is a Python convention that identifiers written in all uppercase characters
are to be treated as constants.
We also need to create a named tuple type for holding the data on each user:
User = collections.namedtuple("User",
"username forename middlename surname id")
We will see how the constants and the User named tuple are used when we look
at the rest of the code.
From the Library of STEPHEN EISEMAN
ptg
150 Chapter 3. Collection Data Types
The program’s overall logic is captured in the main() function:
def main():
if len(sys.argv) == 1 or sys.argv[1] in {"-h", "--help"}:
print("usage: {0} file1 [file2 [... fileN]]".format(
sys.argv[0]))
sys.exit()
usernames = set()
users = {}
for filename in sys.argv[1:]:
for line in open(filename, encoding="utf8"):
line = line.rstrip()
if line:
user = process_line(line, usernames)
users[(user.surname.lower(), user.forename.lower(),
user.id)] = user
print_users(users)
If the user doesn’t provide any filenames on the command line, or if they type
“-h” or “--help” on the command line, we simply print a usage message and
terminate the program.
For each line read, we strip off any trailing whitespace (e.g., \n) and process
only nonempty lines. This means that if the data file contains blank lines they
will be safely ignored.
We keep track of all the allocated usernames in the usernames set to ensure that
we don’t create any duplicates. The data itself is held in the users dictionary,
with each user (member of the staff) stored as a dictionary item whose key is
a tuple of the user’s surname, forename, and ID, and whose value is a named
tuple of type User.Using a tuple of the user’s surname, forename, and ID for the
dictionary’s keys means that if we call sorted() on the dictionary, the iterable
returned will be in the order we want (i.e., surname, forename, ID), without us
having to provide a key function.
def process_line(line, usernames):
fields = line.split(":")
username = generate_username(fields, usernames)
user = User(username, fields[FORENAME], fields[MIDDLENAME],
fields[SURNAME], fields[ID])
return user
Since the data format for each record is so simple, and because we’ve already
stripped the trailing whitespace from the line, we can extract the fields simply
by splitting on the colons. We pass the fields and the usernames set to the
generate_username() function, and then we create an instance of the User named
From the Library of STEPHEN EISEMAN
ptg
Examples 151
tuple type which we then return to the caller (main()), which inserts the user
into the users dictionary, ready for printing.
If we had not created suitable constants to hold the index positions, we would
be reduced to using numeric indexes, for example:
user = User(username, fields[1], fields[2], fields[3], fields[0])
Although this is certainly shorter, it is poor practice. First it isn’t clear to
future maintainers what each field is, and second it is vulnerable to data file
format changes—if the order or number of fields in a record changes, this code
will break everywhere it is used. But by using named constants in the face of
changes to the record struture, we would have to change only the values of the
constants, and all uses of the constants would continue to work.
def generate_username(fields, usernames):
username = ((fields[FORENAME][0] + fields[MIDDLENAME][:1] +
fields[SURNAME]).replace("-", "").replace("'", ""))
username = original_name = username[:8].lower()
count = 1
while username in usernames:
username = "{0}{1}".format(original_name, count)
count += 1
usernames.add(username)
return username
We make a first attempt at creating a username by concatenating the first letter
of the forename, the first letter of the middle name, and the whole surname,
and deleting any hyphens or single quotes from the resultant string. The code
for getting the first letter of the middle name is quite subtle. If we had used
fields[MIDDLENAME][0] we would get an IndexError exception for empty middle
names. But by using a slice we get the first letter if there is one, or an empty
string otherwise.
Next we make the username lowercase and no more than eight characters long.
If the username is in use (i.e., it is in the usernames set), we try the username
with a “1” tacked on at the end, and if that is in use we try with a “2”, and so
on until we get one that isn’t in use. Then we add the username to the set of
usernames and return the username to the caller.
def print_users(users):
namewidth = 32
usernamewidth = 9
print("{0:<{nw}} {1:^6} {2:{uw}}".format(
"Name", "ID", "Username", nw=namewidth, uw=usernamewidth))
print("{0:-<{nw}} {0:-<6} {0:-<{uw}}".format(
"", nw=namewidth, uw=usernamewidth))
From the Library of STEPHEN EISEMAN
ptg
152 Chapter 3. Collection Data Types
for key in sorted(users):
user = users[key]
initial = ""
if user.middlename:
initial =""+ user.middlename[0]
name = "{0.surname}, {0.forename}{1}".format(user, initial)
print("{0:.<{nw}} ({1.id:4}) {1.username:{uw}}".format(
name, user, nw=namewidth, uw=usernamewidth))
Once all the records have been processed, the print_users() function is called,
with the users dictionary passed as its parameter.
str. The first print() statement prints the column titles, and the second
format()

print()
statement prints hyphens under each title. This second statement’s str.
format() call is slightly subtle. The string we give to be printed is "", that is, the
empty string—we get the hyphens by printing the empty string padded with
hyphens to the given widths.
Next we use a for … in loop to print the details of each user, extracting the
key for each user’s dictionary item in sorted order. For convenience we create
the user variable so that we don’t have to keep writing users[key] throughout
the rest of the function. In the loop’s first call to str.format() we set the name
variable to the user’s name in surname, forename (and optional initial) form.
We access items in the user named tuple by name. Once we have the user’s
name as a single string we print the user’s details, constraining each column,
(name, ID, username) to the widths we want.
The complete program (which differs from what we have reviewed only
in that it has some initial comment lines and some imports) is in generate_usernames.py.
The program’s structure—read in a data file, process each
record, write output—is one that is very frequently used, and we will meet it
again in the next example.





import collections
import sys

ID, FORENAME, MIDDLENAME, SURNAME, DEPARTMENT = range(5)

#create a named tuple type for holding the data on each user
User = collections.namedtuple("User","username forename middlename surname id")

def main():
    #if they type “-h” or “--help” on the command line, we simply print a usage message

    if len(sys.argv) == 1 or sys.argv[1] in {"-h", "--help"}:
        print("usage: {0} file1 [file2 [... fileN]]".format(
            sys.argv[0]))
        sys.exit()


        usernames = set()
        users = {}
        for filename in sys.argv[1:]:
            for line in open(filename, encoding="utf8"):
                line = line.rstrip()
                if line:
                    user = process_line(line, usernames)
                    users[(user.surname.lower(), user.forename.lower(),
                           user.id)] = user
        print_users(users)



def process_line(line, usernames):
    fields = line.split(":")
    username = generate_username(fields, usernames)
    user = User(username, fields[FORENAME], fields[MIDDLENAME],
                fields[SURNAME], fields[ID])
    return user


def generate_username(fields, usernames):
    username = ((fields[FORENAME][0] + fields[MIDDLENAME][:1] +
                 fields[SURNAME]).replace("-", "").replace("'", ""))
    username = original_name = username[:8].lower()
    count = 1
    while username in usernames:
        username = "{0}{1}".format(original_name, count)
        count += 1
    usernames.add(username)
    return username

def print_users(users):
    namewidth = 32
    usernamewidth = 9

    print("{0:<{nw}} {1:^6} {2:{uw}}".format(
          "Name", "ID", "Username", nw=namewidth, uw=usernamewidth))
    print("{0:-<{nw}} {0:-<6} {0:-<{uw}}".format(
          "", nw=namewidth, uw=usernamewidth))

    for key in sorted(users):
        user = users[key]
        initial = ""
        if user.middlename:
            initial = " " + user.middlename[0]
        name = "{0.surname}, {0.forename}{1}".format(user, initial)
        print("{0:.<{nw}} ({1.id:4}) {1.username:{uw}}".format(
              name, user, nw=namewidth, uw=usernamewidth))

main()

---------------------------------------------------------------------------------------------------------------------------------------

Modify the generate_usernames.py program so that it prints the details of
two users per line, limiting names to 17 characters and outputting a form
feed character after every 64 lines, with the column titles printed at the
start of every page. Here’s a sample of the expected output:

Name ID Username Name ID Username
----------------- ------ --------- ----------------- ------ ---------
Aitkin, Shatha... (2370) saitkin Alderson, Nicole. (8429) nalderso
Allison, Karma... (8621) kallison Alwood, Kole E... (2095) kealwood
Annie, Neervana.. (2633) nannie Apperson, Lucyann (7282) leappers

This is challenging. You’ll need to keep the column titles in variables so
that they can be printed when needed, and you’ll need to tweak the format
specifications to accommodate the narrower names. One way to achieve
pagination is to write all the output items to a list and then iterate over
the list using striding to get the left- and right-hand items, and using zip()
to pair them up. A solution is provided in generate_usernames_ans.py and
a longer sample data file is provided in data/users2.txt.



import collections
import sys

ID, FORENAME, MIDDLENAME, SURNAME, DEPARTMENT = range(5)

#create a named tuple type for holding the data on each user
User = collections.namedtuple("User","username forename middlename surname id")

def main():
    #if they type “-h” or “--help” on the command line, we simply print a usage message

    if len(sys.argv) == 1 or sys.argv[1] in {"-h", "--help"}:
        print("usage: {0} file1 [file2 [... fileN]]".format(
            sys.argv[0]))
        sys.exit()


        usernames = set()
        users = {}
        for filename in sys.argv[1:]:
            for line in open(filename, encoding="utf8"):
                line = line.rstrip()
                if line:
                    user = process_line(line, usernames)
                    users[(user.surname.lower(), user.forename.lower(),
                           user.id)] = user
        print_users(users)



def process_line(line, usernames):
    fields = line.split(":")
    username = generate_username(fields, usernames)
    user = User(username, fields[FORENAME], fields[MIDDLENAME],
                fields[SURNAME], fields[ID])
    return user


def generate_username(fields, usernames):
    username = ((fields[FORENAME][0] + fields[MIDDLENAME][:1] +
                 fields[SURNAME]).replace("-", "").replace("'", ""))
    username = original_name = username[:8].lower()
    count = 1
    while username in usernames:
        username = "{0}{1}".format(original_name, count)
        count += 1
    usernames.add(username)
    return username

def by_surname_forename(user):
    return user.surname.lower(), user.forename.lower(), user.id

def print_users(users):
    namewidth = 17
    usernamewidth = 9
    columngap = " " * 2

    headline1 = "{0:<{nw}} {1:^6} {2:{uw}}".format("Name", "ID",
            "Username", nw=namewidth, uw=usernamewidth)
    headline2 = "{0:-<{nw}} {0:-<6} {0:-<{uw}}".format("",
            nw=namewidth, uw=usernamewidth)
    header = (headline1 + columngap + headline1 + "\n" +
              headline2 + columngap + headline2)

    lines = []
    for key in sorted(users):
        user = users[key]
        initial = ""
        if user.middlename:
            initial = " " + user.middlename[0]
        name = "{0.surname}, {0.forename}{1}".format(user, initial)
        lines.append("{0:.<{nw}.{nw}} ({1.id:4}) "
                     "{1.username:{uw}}".format(name, user,
                     nw=namewidth, uw=usernamewidth))

    lines_per_page = 64
    lino = 0
    for left, right in zip(lines[::2], lines[1::2]):
        if lino == 0:
            print(header)
        print(left + columngap + right)
        lino += 1
        if lino == lines_per_page:
            print("\f")
            lino = 0
    if lines[-1] != right:
        print(lines[-1])

main()


---------------------------------------------------------------------------------------------------------------------------------------

import sys


sites = {}
for filename in sys.argv[1:]:
    for line in open(filename):
        i = 0
        while True:
            site = None
            i = line.find("http://", i)
            if i > -1:
                i += len("http://")
                for j in range(i, len(line)):
                    if not (line[j].isalnum() or line[j] in ".-"):
                        site = line[i:j].lower()
                        break
                if site and "." in site:
                    sites.setdefault(site, set()).add(filename)
                i = j
            else:
                break

for site in sorted(sites):
    print("{0} is referred to in:".format(site))
    for filename in sorted(sites[site], key=str.lower):
        print("    {0}".format(filename))


---------------------------------------------------------------------------------------------------------------------------------------

Modify the external_sites.py program to use a default dictionary. This is
an easy change requiring an additional import, and changes to just two
other lines. A solution is provided in external_sites_ans.py.

import collections
import sys


sites = collections.defaultdict(set)
for filename in sys.argv[1:]:
    for line in open(filename):
        i = 0
        while True:
            site = None
            i = line.find("http://", i)
            if i > -1:
                i += len("http://")
                for j in range(i, len(line)):
                    if not (line[j].isalnum() or line[j] in ".-"):
                        site = line[i:j].lower()
                        break
                if site and "." in site:
                    sites[site].add(filename)
                i = j
            else:
                break

for site in sorted(sites):
    print("{0} is referred to in:".format(site))
    for filename in sorted(sites[site], key=str.lower):
        print("    {0}".format(filename))

---------------------------------------------------------------------------------------------------------------------------------------
import random


def get_forenames_and_surnames():
    forenames = []
    surnames = []
    for names, filename in ((forenames, "data/forenames.txt"),
                            (surnames, "data/surnames.txt")):
        for name in open(filename, encoding="utf8"):
            names.append(name.rstrip())
    return forenames, surnames


forenames, surnames = get_forenames_and_surnames()
fh = open("test-names1.txt", "w", encoding="utf8")
for i in range(100):
    line = "{0} {1}\n".format(random.choice(forenames),
                              random.choice(surnames))
    fh.write(line)


---------------------------------------------------------------------------------------------------------------------------------------
import random


def get_forenames_and_surnames():
    forenames = []
    surnames = []
    for names, filename in ((forenames, "data/forenames.txt"),
                            (surnames, "data/surnames.txt")):
        for name in open(filename, encoding="utf8"):
            names.append(name.rstrip())
    return forenames, surnames


forenames, surnames = get_forenames_and_surnames()
fh = open("test-names2.txt", "w", encoding="utf8")
limit = 100
years = list(range(1970, 2013)) * 3
for year, forename, surname in zip(
        random.sample(years, limit),
        random.sample(forenames, limit),
        random.sample(surnames, limit)):
    name = "{0} {1}".format(forename, surname)
    fh.write("{0:.<25}.{1}\n".format(name, year))

---------------------------------------------------------------------------------------------------------------------------------------
import sys


if len(sys.argv) < 3:
    print("usage: grepword.py word infile1 [infile2 [... infileN]]")
    sys.exit()

word = sys.argv[1]
for filename in sys.argv[2:]:
    for lino, line in enumerate(open(filename), start=1):
        if word in line:
            print("{0}:{1}:{2:.40}".format(filename, lino,
                                           line.rstrip()))

---------------------------------------------------------------------------------------------------------------------------------------

import collections
import math
import sys


Statistics = collections.namedtuple("Statistics",
                                    "mean mode median std_dev")


def main():
    if len(sys.argv) == 1 or sys.argv[1] in {"-h", "--help"}:
        print("usage: {0} file1 [file2 [... fileN]]".format(
              sys.argv[0]))
        sys.exit()

    numbers = []
    frequencies = collections.defaultdict(int)
    for filename in sys.argv[1:]:
        read_data(filename, numbers, frequencies)
    if numbers:
        statistics = calculate_statistics(numbers, frequencies)
        print_results(len(numbers), statistics)
    else:
        print("no numbers found")


def read_data(filename, numbers, frequencies):
    for lino, line in enumerate(open(filename, encoding="ascii"),
                                start=1):
        for x in line.split():
            try:
                number = float(x)
                numbers.append(number)
                frequencies[number] += 1
            except ValueError as err:
                print("{filename}:{lino}: skipping {x}: {err}".format(
                      **locals()))


def calculate_statistics(numbers, frequencies):
    mean = sum(numbers) / len(numbers)
    mode = calculate_mode(frequencies, 3)
    median = calculate_median(numbers)
    std_dev = calculate_std_dev(numbers, mean)
    return Statistics(mean, mode, median, std_dev)


def calculate_mode(frequencies, maximum_modes):
    highest_frequency = max(frequencies.values())
    mode = [number for number, frequency in frequencies.items()
            if frequency == highest_frequency]
    if not (1 <= len(mode) <= maximum_modes):
        mode = None
    else:
        mode.sort()
    return mode


def calculate_median(numbers):
    numbers = sorted(numbers)
    middle = len(numbers) // 2
    median = numbers[middle]
    if len(numbers) % 2 == 0:
        median = (median + numbers[middle - 1]) / 2
    return median


def calculate_std_dev(numbers, mean):
    total = 0
    for number in numbers:
        total += ((number - mean) ** 2)
    variance = total / (len(numbers) - 1)
    return math.sqrt(variance)


def print_results(count, statistics):
    real = "9.2f"

    if statistics.mode is None:
        modeline = ""
    elif len(statistics.mode) == 1:
        modeline = "mode      = {0:{fmt}}\n".format(
                statistics.mode[0], fmt=real)
    else:
        modeline = ("mode      = [" +
                    ", ".join(["{0:.2f}".format(m)
                    for m in statistics.mode]) + "]\n")

    print("""\
count     = {0:6}
mean      = {mean:{fmt}}
median    = {median:{fmt}}
{1}\
std. dev. = {std_dev:{fmt}}""".format(
    count, modeline, fmt=real, **statistics._asdict()))


main()
---------------------------------------------------------------------------------------------------------------------------------------

import string
import sys

words = {}
strip = string.whitespace + string.punctuation + string.digits + "\"'"
for filename in sys.argv[1:]:
    for line in open(filename):
        for word in line.lower().split():
            word = word.strip(strip)
            if len(word) > 2:
                words[word] = words.get(word, 0) + 1
for word in sorted(words):
    print("'{0}' occurs {1} times".format(word, words[word]))
---------------------------------------------------------------------------------------------------------------------------------------
import collections
import string
import sys


words = collections.defaultdict(int)
strip = string.whitespace + string.punctuation + string.digits + "\"'"
for filename in sys.argv[1:]:
    for line in open(filename):
        for word in line.lower().split():
            word = word.strip(strip)
            if len(word) > 2:
                words[word] += 1
for word in sorted(words):
    print("'{0}' occurs {1} times".format(word, words[word]))


-----------------------------------------------------------------------------------------------------------------------------------------

import collections
import string
import sys


def by_value(item):
    return item[1]


words = collections.defaultdict(int)
strip = string.whitespace + string.punctuation + string.digits + "\"'"
for filename in sys.argv[1:]:
    for line in open(filename):
        for word in line.lower().split():
            word = word.strip(strip)
            if len(word) > 2:
                words[word] += 1
for word, count in sorted(words.items(), key=by_value):
    print("'{0}' occurs {1} times".format(word, count))