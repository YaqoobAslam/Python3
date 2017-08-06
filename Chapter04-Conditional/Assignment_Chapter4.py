checktags.py

import string
import sys

class InvalidEntityError(Exception): pass
class InvalidNumericEntityError(InvalidEntityError): pass
class InvalidAlphaEntityError(InvalidEntityError): pass
class InvalidTagContentError(Exception): pass


def parse(filename, skip_on_first_error=False):
    HEXDIGITS = frozenset("0123456789ABCDEFabcdef")
    NORMAL, PARSING_TAG, PARSING_ENTITY = range(3)
    state = NORMAL
    entity = ""
    fh = None
    try:
        fh = open(filename, encoding="utf8")
        errors = False
        for lino, line in enumerate(fh, start=1):
            for column, c in enumerate(line, start=1):
                try:
                    if state == NORMAL:
                        if c == "<":
                            state = PARSING_TAG
                        elif c == "&":
                            entity = ""
                            state = PARSING_ENTITY
                    elif state == PARSING_TAG:
                        if c == ">":
                            state = NORMAL
                        elif c == "<":
                            raise InvalidTagContentError()
                    elif state == PARSING_ENTITY:
                        if c == ";":
                            if entity.startswith("#"):
                                if frozenset(entity[1:]) - HEXDIGITS:
                                    raise InvalidNumericEntityError()
                            elif not entity.isalpha():
                                raise InvalidAlphaEntityError()
                            entity = ""
                            state = NORMAL
                        else:
                            if entity.startswith("#"):
                                if c not in HEXDIGITS:
                                    raise InvalidNumericEntityError()
                            elif (entity and
                                  c not in string.ascii_letters):
                                raise InvalidAlphaEntityError()
                            entity += c
                except (InvalidEntityError,
                        InvalidTagContentError) as err:
                    if isinstance(err, InvalidNumericEntityError):
                        error = "invalid numeric entity"
                    elif isinstance(err, InvalidAlphaEntityError):
                        error = "invalid alphabetic entity"
                    elif isinstance(err, InvalidTagContentError):
                        error = "invalid tag"
                    print("ERROR {0} in {1} on line {2} column {3}"
                          .format(error, filename, lino, column))
                    if skip_on_first_error:
                        raise
                    entity = ""
                    state = NORMAL
                    errors = True
        if state == PARSING_TAG:
            raise EOFError("missing '>' at end of " + filename)
        elif state == PARSING_ENTITY:
            raise EOFError("missing ';' at end of " + filename)
        if not errors:
            print("OK", filename)
    except (InvalidEntityError, InvalidTagContentError):
        pass # Already handled
    except EOFError as err:
        print("ERROR unexpected EOF:", err)
    except EnvironmentError as err:
        print(err)
    finally:
        if fh is not None:
            fh.close()


if len(sys.argv) < 2:
    print("usage: checktags.py infile1 [infile2 [... infileN]]")
    sys.exit()

for filename in sys.argv[1:]:
    parse(filename)
----------------------------------------------------------------------------------------------------------------------------------------------
 digit_names.py

import sys


Language = "en"

ENGLISH = {0: "zero", 1: "one", 2: "two", 3: "three", 4: "four",
           5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}
FRENCH = {0: "zero", 1: "un", 2: "deux", 3: "trois", 4: "quatre",
          5: "cinq", 6: "six", 7: "sept", 8: "huit", 9: "neuf"}


def main():
    if len(sys.argv) == 1 or sys.argv[1] in {"-h", "--help"}:
        print("usage: {0} [en|fr] number".format(sys.argv[0]))
        sys.exit()

    args = sys.argv[1:]
    if args[0] in {"en", "fr"}:
        global Language
        Language = args.pop(0)
    print_digits(args.pop(0))


def print_digits(digits):
    dictionary = ENGLISH if Language == "en" else FRENCH
    for digit in digits:
        print(dictionary[int(digit)], end=" ")
    print()


main()

----------------------------------------------------------------------------------------------------------------------------------------------

import os


YES = frozenset({"y", "Y", "yes", "Yes", "YES"})


def main():
    dirty = False
    items = []

    filename, items = choose_file()
    if not filename:
        print("Cancelled")
        return

    while True:
        print("\nList Keeper\n")
        print_list(items)
        choice = get_choice(items, dirty)

        if choice in "Aa":
            dirty = add_item(items, dirty)
        elif choice in "Dd":
            dirty = delete_item(items, dirty)
        elif choice in "Ss":
            dirty = save_list(filename, items)
        elif choice in "Qq":
            if (dirty and (get_string("Save unsaved changes (y/n)",
                                      "yes/no", "y") in YES)):
                save_list(filename, items, True)
            break


def choose_file():
    enter_filename = False
    print("\nList Keeper\n")
    files = [x for x in os.listdir(".") if x.endswith(".lst")]
    if not files:
        enter_filename = True
    if not enter_filename:
        print_list(files)
        index = get_integer("Specify file's number (or 0 to create "
                            "a new one)", "number", maximum=len(files),
                            allow_zero=True)
        if index == 0:
            enter_filename = True
        else:
            filename = files[index - 1]
            items = load_list(filename)
    if enter_filename:
        filename = get_string("Choose filename", "filename")
        if not filename.endswith(".lst"):
            filename += ".lst"
        items = []
    return filename, items



def print_list(items):
    if not items:
        print("-- no items are in the list --")
    else:
        width = 1 if len(items) < 10 else 2 if len(items) < 100 else 3
        for i, item in enumerate(items):
            print("{0:{width}}: {item}".format(i + 1, **locals()))
    print()


def get_choice(items, dirty):
    while True:
        if items:
            if dirty:
                menu = "[A]dd  [D]elete  [S]ave  [Q]uit"
                valid_choices = "AaDdSsQq"
            else:
                menu = "[A]dd  [D]elete  [Q]uit"
                valid_choices = "AaDdQq"
        else:
            menu = "[A]dd  [Q]uit"
            valid_choices = "AaQq"
        choice = get_string(menu, "choice", "a")

        if choice not in valid_choices:
            print("ERROR: invalid choice--enter one of '{0}'".format(
                  valid_choices))
            input("Press Enter to continue...")
        else:
            return choice


def add_item(items, dirty):
    item = get_string("Add item", "item")
    if item:
        items.append(item)
        items.sort(key=str.lower)
        return True
    return dirty


def delete_item(items, dirty):
    index = get_integer("Delete item number (or 0 to cancel)",
                        "number", maximum=len(items),
                        allow_zero=True)
    if index != 0:
        del items[index - 1]
        return True
    return dirty


def load_list(filename):
    items = []
    fh = None
    try:
        for line in open(filename, encoding="utf8"):
            items.append(line.rstrip())
    except EnvironmentError as err:
        print("ERROR: failed to load {0}: {1}".format(filename, err))
        return []
    finally:
        if fh is not None:
            fh.close()
    return items


def save_list(filename, items, terminating=False):
    fh = None
    try:
        fh = open(filename, "w", encoding="utf8")
        fh.write("\n".join(items))
        fh.write("\n")
    except EnvironmentError as err:
        print("ERROR: failed to save {0}: {1}".format(filename, err))
        return True
    else:
        print("Saved {0} item{1} to {2}".format(len(items),
              ("s" if len(items) != 1 else ""), filename))
        if not terminating:
            input("Press Enter to continue...")
        return False
    finally:
        if fh is not None:
            fh.close()


def get_string(message, name="string", default=None,
               minimum_length=0, maximum_length=80):
    message += ": " if default is None else " [{0}]: ".format(default)
    while True:
        try:
            line = input(message)
            if not line:
                if default is not None:
                    return default
                if minimum_length == 0:
                    return ""
                else:
                    raise ValueError("{0} may not be empty".format(
                                     name))
            if not (minimum_length <= len(line) <= maximum_length):
                raise ValueError("{name} must have at least "
                        "{minimum_length} and at most "
                        "{maximum_length} characters".format(
                        **locals()))
            return line
        except ValueError as err:
            print("ERROR", err)


def get_integer(message, name="integer", default=None, minimum=0,
                maximum=100, allow_zero=True):

    class RangeError(Exception): pass

    message += ": " if default is None else " [{0}]: ".format(default)
    while True:
        try:
            line = input(message)
            if not line and default is not None:
                return default
            i = int(line)
            if i == 0:
                if allow_zero:
                    return i
                else:
                    raise RangeError("{0} may not be 0".format(name))
            if not (minimum <= i <= maximum):
                raise RangeError("{name} must be between {minimum} "
                        "and {maximum} inclusive{0}".format(
                        " (or 0)" if allow_zero else "", **locals()))
            return i
        except RangeError as err:
            print("ERROR", err)
        except ValueError as err:
            print("ERROR {0} must be an integer".format(name))


main()

----------------------------------------------------------------------------------------------------------------------------------------------

import datetime
import xml.sax.saxutils


COPYRIGHT_TEMPLATE = "Copyright (c) {0} {1}. All rights reserved."

STYLESHEET_TEMPLATE = ('<link rel="stylesheet" type="text/css" '
                       'media="all" href="{0}" />\n')

HTML_TEMPLATE = """<?xml version="1.0"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" \
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
<title>{title}</title>
<!-- {copyright} -->
<meta name="Description" content="{description}" />
<meta name="Keywords" content="{keywords}" />
<meta equiv="content-type" content="text/html; charset=utf-8" />
{stylesheet}\
</head>
<body>
</body>
</html>
"""

class CancelledError(Exception): pass


def main():
    information = dict(name=None, year=datetime.date.today().year,
                       filename=None, title=None, description=None,
                       keywords=None, stylesheet=None)
    while True:
        try:
            print("\nMake HTML Skeleton\n")
            populate_information(information)
            make_html_skeleton(**information)
        except CancelledError:
            print("Cancelled")
        if (get_string("\nCreate another (y/n)?", default="y").lower()
            not in {"y", "yes"}):
            break


def populate_information(information):
    name = get_string("Enter your name (for copyright)", "name",
                      information["name"])
    if not name:
        raise CancelledError()
    year = get_integer("Enter copyright year", "year",
                       information["year"], 2000,
                       datetime.date.today().year + 1, True)
    if year == 0:
        raise CancelledError()
    filename = get_string("Enter filename", "filename")
    if not filename:
        raise CancelledError()
    if not filename.endswith((".htm", ".html")):
        filename += ".html"
    title = get_string("Enter title", "title")
    if not title:
        raise CancelledError()
    description = get_string("Enter description (optional)",
                             "description")
    keywords = []
    while True:
        keyword = get_string("Enter a keyword (optional)", "keyword")
        if keyword:
            keywords.append(keyword)
        else:
            break
    stylesheet = get_string("Enter the stylesheet filename "
                            "(optional)", "stylesheet")
    if stylesheet and not stylesheet.endswith(".css"):
        stylesheet += ".css"
    information.update(name=name, year=year, filename=filename,
                       title=title, description=description,
                       keywords=keywords, stylesheet=stylesheet)


def make_html_skeleton(year, name, title, description, keywords,
                       stylesheet, filename):
    copyright = COPYRIGHT_TEMPLATE.format(year,
                                    xml.sax.saxutils.escape(name))
    title = xml.sax.saxutils.escape(title)
    description = xml.sax.saxutils.escape(description)
    keywords = ",".join([xml.sax.saxutils.escape(k)
                         for k in keywords]) if keywords else ""
    stylesheet = (STYLESHEET_TEMPLATE.format(stylesheet)
                  if stylesheet else "")
    html = HTML_TEMPLATE.format(**locals())
    fh = None
    try:
        fh = open(filename, "w", encoding="utf8")
        fh.write(html)
    except EnvironmentError as err:
        print("ERROR", err)
    else:
        print("Saved skeleton", filename)
    finally:
        if fh is not None:
            fh.close()


def get_string(message, name="string", default=None,
               minimum_length=0, maximum_length=80):
    message += ": " if default is None else " [{0}]: ".format(default)
    while True:
        try:
            line = input(message)
            if not line:
                if default is not None:
                    return default
                if minimum_length == 0:
                    return ""
                else:
                    raise ValueError("{0} may not be empty".format(
                                     name))
            if not (minimum_length <= len(line) <= maximum_length):
                raise ValueError("{name} must have at least "
                        "{minimum_length} and at most "
                        "{maximum_length} characters".format(
                        **locals()))
            return line
        except ValueError as err:
            print("ERROR", err)


def get_integer(message, name="integer", default=None, minimum=0,
                maximum=100, allow_zero=True):

    class RangeError(Exception): pass

    message += ": " if default is None else " [{0}]: ".format(default)
    while True:
        try:
            line = input(message)
            if not line and default is not None:
                return default
            i = int(line)
            if i == 0:
                if allow_zero:
                    return i
                else:
                    raise RangeError("{0} may not be 0".format(name))
            if not (minimum <= i <= maximum):
                raise RangeError("{name} must be between {minimum} "
                        "and {maximum} inclusive{0}".format(
                        " (or 0)" if allow_zero else "", **locals()))
            return i
        except RangeError as err:
            print("ERROR", err)
        except ValueError as err:
            print("ERROR {0} must be an integer".format(name))


main()

----------------------------------------------------------------------------------------------------------------------------------------------

import os
import sys


def read_data(filename):
    lines = []
    fh = None
    try:
        fh = open(filename, encoding="utf8")
        for line in fh:
            if line.strip():
                lines.append(line)
    except (IOError, OSError) as err:
        print(err)
        return []
    finally:
        if fh is not None:
            fh.close()
    return lines


def write_data(lines, filename):
    fh = None
    try:
        fh = open(filename, "w", encoding="utf8")
        for line in lines:
            fh.write(line)
    except EnvironmentError as err:
        print(err)
    finally:
        if fh is not None:
            fh.close()


if len(sys.argv) < 2:
    print("usage: noblanks.py infile1 [infile2 [... infileN]]")
    sys.exit()

for filename in sys.argv[1:]:
    lines = read_data(filename)
    if lines:
        write_data(lines, os.path.splitext(filename)[0] + ".nb")

----------------------------------------------------------------------------------------------------------------------------------------------

import string


def is_balanced(text, brackets="()[]{}<>"):
    """Returns True if all the brackets in the text are balanced
    For each pair of brackets, the left and right bracket characters
    must be different.
    >>> is_balanced("no brackets at all")
    True
    >>> is_balanced("<b>bold</b>")
    True
    >>> is_balanced("[<b>(some {thing}) goes</b>]")
    True
    >>> is_balanced("<b>[not (where {it}) is}]</b>")
    False
    >>> is_balanced("(not (<tag>(like) (anything)</tag>)")
    False
    """
    counts = {}
    left_for_right = {}
    for left, right in zip(brackets[::2], brackets[1::2]):
        assert left != right, "the bracket characters must differ"
        counts[left] = 0
        left_for_right[right] = left
    for c in text:
        if c in counts:
            counts[c] += 1
        elif c in left_for_right:
            left = left_for_right[c]
            if counts[left] == 0:
                return False
            counts[left] -= 1
    return not any(counts.values())


def shorten(text, length=25, indicator="..."):
    """Returns text or a truncated copy with the indicator added
    text is any string; length is the maximum length of the returned
    string (including any indicator); indicator is the string added at
    the end to indicate that the text has been shortened
    >>> shorten("Second Variety")
    'Second Variety'
    >>> shorten("Voices from the Street", 17)
    'Voices from th...'
    >>> shorten("Radio Free Albemuth", 10, "*")
    'Radio Fre*'
    """
    if len(text) > length:
        text = text[:length - len(indicator)] + indicator
    return text


def simplify(text, whitespace=string.whitespace, delete=""):
    r"""Returns the text with multiple spaces reduced to single spaces
    The whitespace parameter is a string of characters, each of which
    is considered to be a space.
    If delete is not empty it should be a string, in which case any
    characters in the delete string are excluded from the resultant
    string.
    >>> simplify(" this    and\n that\t too")
    'this and that too'
    >>> simplify("  Washington   D.C.\n")
    'Washington D.C.'
    >>> simplify("  Washington   D.C.\n", delete=",;:.")
    'Washington DC'
    >>> simplify(" disemvoweled ", delete="aeiou")
    'dsmvwld'
    """
    result = []
    word = ""
    for char in text:
        if char in delete:
            continue
        elif char in whitespace:
            if word:
                result.append(word)
                word = ""
        else:
            word += char
    if word:
        result.append(word)
    return " ".join(result)


def insert_at(string, position, insert):
    """Returns a copy of string with insert inserted at the position
    >>> string = "ABCDE"
    >>> result = []
    >>> for i in range(-2, len(string) + 2):
    ...     result.append(insert_at(string, i, "-"))
    >>> result[:5]
    ['ABC-DE', 'ABCD-E', '-ABCDE', 'A-BCDE', 'AB-CDE']
    >>> result[5:]
    ['ABC-DE', 'ABCD-E', 'ABCDE-', 'ABCDE-']
    """
    return string[:position] + insert + string[position:]


def dummy_insert_at(string, position, insert):
    """Returns a copy of string with insert inserted at the position
    >>> string = "ABCDE"
    >>> result = []
    >>> for i in range(-2, len(string) + 2):
    ...     result.append(insert_at(string, i, "-"))
    >>> result[:5]
    ['ABC-DE', 'ABCD-E', '-ABCDE', 'A-BCDE', 'AB-CDE']
    >>> result[5:]
    ['ABC-DE', 'ABCD-E', 'ABCDE-', 'ABCDE-']
    """
    return string


if __name__ == "__main__":
    import doctest
    doctest.testmod()

----------------------------------------------------------------------------------------------------------------------------------------------

import functools
import inspect
import logging
import os
import string
import sys
import tempfile
import unicodedata


def complete_comparisons(cls):
    """A class decorator that completes a class's comparisons operators.
    The decorated class will have the operators <, <=, ==, !=, >=, >,
    assuming it already has <, and ideally == too. If the class doesn't
    even have < an assertion error is raised.
    >>> @complete_comparisons
    ... class AClass(): pass
    Traceback (most recent call last):
    ...
    AssertionError: AClass must define < and ideally ==
    >>> @complete_comparisons
    ... class Lt():
    ...     def __init__(self, x=""):
    ...         self.x = x
    ...     def __str__(self):
    ...         return self.x
    ...     def __lt__(self, other):
    ...         return str(self) < str(other) 
    >>> a = Lt("a")
    >>> b = Lt("b")
    >>> b2 = Lt("b")
    >>> (a < b, a <= b, a == b, a !=b, a >= b, a > b)
    (True, True, False, True, False, False)
    >>> (b < b2, b <= b2, b == b2, b != b2, b >= b2, b > b2)
    (False, True, True, False, True, False)
    >>> @complete_comparisons
    ... class LtEq():
    ...     def __init__(self, x=""):
    ...         self.x = x
    ...     def __str__(self):
    ...         return self.x
    ...     def __lt__(self, other):
    ...         return str(self) < str(other) 
    ...     def __eq__(self, other):
    ...         return str(self) == str(other) 
    >>> a = LtEq("a")
    >>> b = LtEq("b")
    >>> b2 = LtEq("b")
    >>> (a < b, a <= b, a == b, a !=b, a >= b, a > b)
    (True, True, False, True, False, False)
    >>> (b < b2, b <= b2, b == b2, b != b2, b >= b2, b > b2)
    (False, True, True, False, True, False)
    """
    assert cls.__lt__ is not object.__lt__, (
            "{0} must define < and ideally ==".format(cls.__name__))
    if cls.__eq__ is object.__eq__:
        cls.__eq__ = lambda self, other: (not
                (cls.__lt__(self, other) or cls.__lt__(other, self)))
    cls.__ne__ = lambda self, other: not cls.__eq__(self, other)
    cls.__gt__ = lambda self, other: cls.__lt__(other, self)
    cls.__le__ = lambda self, other: not cls.__lt__(other, self)
    cls.__ge__ = lambda self, other: not cls.__lt__(self, other)
    return cls


def delegate(attribute_name, method_names):
    """Passes the call to the attribute called attribute_name for
    every method listed in method_names.
    (See SortedListP.py for an example.)
    """
    def decorator(cls):
        nonlocal attribute_name
        if attribute_name.startswith("__"):
            attribute_name = "_" + cls.__name__ + attribute_name
        for name in method_names:
            setattr(cls, name, eval("lambda self, *a, **kw: "
                                    "self.{0}.{1}(*a, **kw)".format(
                                    attribute_name, name)))
        return cls
    return decorator



def equal_float(a, b, decimals=None):
    """Returns True if a and b are equal to the limits of the machine's
    accuracy or to the specified number of decimal places if specified
    >>> equal_float(.1, .1), equal_float(.000000000001, .000000000001)
    (True, True)
    >>> equal_float(.00000000000101, .00000000000102, 13)
    True
    >>> equal_float(.00000000000101, .00000000000102)
    False
    >>> equal_float(.00000000000101, .00000000000102, 9)
    True
    """
    if decimals is not None:
        a = round(a, decimals)
        b = round(b, decimals)
    return abs(a - b) <= (sys.float_info.epsilon * min(abs(a), abs(b)))


def equal_float_old(a, b, epsilon=None):
    """Returns True if a and b are equal to the limits of the machine's
    accuracy or to the limit of epsilon if given
    >>> equal_float_old(.1, .1), equal_float_old(.000000000001, .000000000001)
    (True, True)
    >>> equal_float_old(.00000000000101, .00000000000102, .0000000000001)
    True
    >>> equal_float_old(.00000000000101, .00000000000102)
    False
    """
    if epsilon is None:
        return abs(a - b) <= (sys.float_info.epsilon * min(abs(a), abs(b)))
    return abs(a - b) <= epsilon


s = lambda x: "" if x == 1 else "s"
s.__doc__ = "Returns 's' for quantities other than 1"


def positive_result(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        assert result >= 0, function.__name__ + "() result isn't >= 0"
        return result
    return wrapper


@positive_result
def discriminant(a, b, c):
    """
    >>> discriminant(1, 2, 3)
    Traceback (most recent call last):
    ...
    AssertionError: discriminant() result isn't >= 0
    >>> discriminant(3, 4, 1)
    4
    >>> discriminant.__name__
    'discriminant'
    """
    return (b ** 2) - (4 * a * c)


def bounded(minimum, maximum):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            if result < minimum:
                return minimum
            elif result > maximum:
                return maximum
            return result
        return wrapper
    return decorator


@bounded(0, 100)
def percent(amount, total):
    """
    >>> percent(512, 4096)
    12.5
    >>> percent(811, 700)
    100
    >>> percent(-7, 91)
    0
    """
    return (amount / total) * 100


def strictly_typed(function):
    annotations = function.__annotations__
    arg_spec = inspect.getfullargspec(function)

    assert "return" in annotations, "missing type for return value"
    for arg in arg_spec.args + arg_spec.kwonlyargs:
        assert arg in annotations, ("missing type for parameter '" +
                                    arg + "'")
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        for name, arg in (list(zip(arg_spec.args, args)) +
                          list(kwargs.items())):
            assert isinstance(arg, annotations[name]), (
                    "expected argument '{0}' of {1} got {2}".format(
                    name, annotations[name], type(arg)))
        result = function(*args, **kwargs)
        assert isinstance(result, annotations["return"]), (
                    "expected return of {0} got {1}".format(
                    annotations["return"], type(result)))
        return result
    return wrapper


if __debug__:
    logger = logging.getLogger("Logger")
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(os.path.join(
                                tempfile.gettempdir(), "logged.log"))
    logger.addHandler(handler)

    def logged(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            log = "called: " + function.__name__ + "("
            log += ", ".join(["{0!r}".format(a) for a in args] +
                             ["{0!s}={1!r}".format(k, v)
                              for k, v in kwargs.items()])
            result = exception = None
            try:
                result = function(*args, **kwargs)
                return result
            except Exception as err:
                exception = err
            finally:
                log += ((") -> " + str(result)) if exception is None
                        else ") {0}: {1}".format(type(exception),
                                                 exception))
                logger.debug(log)
                if exception is not None:
                    raise exception
        return wrapper
else:
    def logged(function):
        return function


def is_unicode_punctuation(s : str) -> bool:
    """
    >>> is_unicode_punctuation("No way!")
    False
    >>> is_unicode_punctuation("@!?*")
    True
    >>> is_unicode_punctuation("@!?*X")
    False
    """
    for c in s:
        if unicodedata.category(c)[0] != "P":
            return False
    return True


def int2base36(integer):
    """Returns integer as a base 36 string
    Use int(string, 36) to do the reverse conversion.
    >>> int2base36(0)
    '0'
    >>> int2base36(35), int("Z", 36)
    ('Z', 35)
    >>> int2base36(36), int("10", 36)
    ('10', 36)
    >>> int2base36(37), int("11", 36)
    ('11', 37)
    >>> int2base36(98712374), int("1MRQYE", 36)
    ('1MRQYE', 98712374)
    >>> int2base36(825170), int("HOPE", 36)
    ('HOPE', 825170)
    """
    DIGITS = string.digits + string.ascii_uppercase
    digits = []
    while integer >= 36:
        integer, modulus = divmod(integer, 36)
        digits.append(DIGITS[modulus])
    digits.append(DIGITS[integer])
    return "".join(reversed(digits))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
