
Account.py
import pickle


class Transaction:

    def __init__(self, amount, date, currency="USD",
                 usd_conversion_rate=1, description=None):
        """
        >>> t = Transaction(100, "2008-12-09")
        >>> t.amount, t.currency, t.usd_conversion_rate, t.usd
        (100, 'USD', 1, 100)
        >>> t = Transaction(250, "2009-03-12", "EUR", 1.53)
        >>> t.amount, t.currency, t.usd_conversion_rate, t.usd
        (250, 'EUR', 1.53, 382.5)
        """
        self.__amount = amount
        self.__date = date
        self.__description = description
        self.__currency = currency
        self.__usd_conversion_rate = usd_conversion_rate


    @property
    def amount(self):
        return self.__amount


    @property
    def date(self):
        return self.__date


    @property
    def description(self):
        return self.__description


    @property
    def currency(self):
        return self.__currency


    @property
    def usd_conversion_rate(self):
        return self.__usd_conversion_rate


    @property
    def usd(self):
        return self.__amount * self.__usd_conversion_rate


class Account:
    """
    >>> import os
    >>> import tempfile
    >>> name = os.path.join(tempfile.gettempdir(), "account01")
    >>> account = Account(name, "Qtrac Ltd.")
    >>> os.path.basename(account.number), account.name,
    ('account01', 'Qtrac Ltd.')
    >>> account.balance, account.all_usd, len(account)
    (0.0, True, 0)
    >>> account.apply(Transaction(100, "2008-11-14"))
    >>> account.apply(Transaction(150, "2008-12-09"))
    >>> account.apply(Transaction(-95, "2009-01-22"))
    >>> account.balance, account.all_usd, len(account)
    (155.0, True, 3)
    >>> account.apply(Transaction(50, "2008-12-09", "EUR", 1.53))
    >>> account.balance, account.all_usd, len(account)
    (231.5, False, 4)
    >>> account.save()
    >>> newaccount = Account(name, "Qtrac Ltd.")
    >>> newaccount.balance, newaccount.all_usd, len(newaccount)
    (0.0, True, 0)
    >>> newaccount.load()
    >>> newaccount.balance, newaccount.all_usd, len(newaccount)
    (231.5, False, 4)
    >>> try:
    ...     os.remove(name + ".acc")
    ... except EnvironmentError:
    ...     pass
    """

    def __init__(self, number, name):
        """Creates a new account with the given number and name
        The number is used as the account's filename.
        """
        self.__number = number
        self.__name = name
        self.__transactions = []
        

    @property
    def number(self):
        "The read-only account number"
        return self.__number


    @property
    def name(self):
        """The account's name
        This can be changed since it is only for human convenience;
        the account number is the true identifier.
        """
        return self.__name

    @name.setter
    def name(self, name):
        assert len(name) > 3, "account name must be at least 4 characters"
        self.__name = name


    def __len__(self):
        "Returns the number of transactions"
        return len(self.__transactions)


    def apply(self, transaction):
        "Applies (adds) the given transaction to the account"
        self.__transactions.append(transaction)


    @property
    def balance(self):
        "Returns the balance in USD"
        total = 0.0
        for transaction in self.__transactions:
            total += transaction.usd
        return total


    @property
    def all_usd(self):
        "Returns True if all transactions are in USD"
        for transaction in self.__transactions:
            if transaction.currency != "USD":
                return False
        return True
         

    def save(self):
        "Saves the account's data in file number.acc"
        fh = None
        try:
            data = [self.number, self.name, self.__transactions]
            fh = open(self.number + ".acc", "wb")
            pickle.dump(data, fh, pickle.HIGHEST_PROTOCOL)
        except (EnvironmentError, pickle.PicklingError) as err:
            raise SaveError(str(err))
        finally:
            if fh is not None:
                fh.close()


    def load(self):
        """Loads the account's data from file number.acc
        All previous data is lost.
        """
        fh = None
        try:
            fh = open(self.number + ".acc", "rb")
            data = pickle.load(fh)
            assert self.number == data[0], "account number doesn't match"
            self.__name, self.__transactions = data[1:]
        except (EnvironmentError, pickle.UnpicklingError) as err:
            raise LoadError(str(err))
        finally:
            if fh is not None:
                fh.close()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
------------------------------------------------------------------------------------------------------------------------------------------------
Circle.py

import math


def distance_from_origin(x, y):
    return math.hypot(x, y)


def edge_distance_from_origin(x, y, radius):
    assert radius > 0
    return distance_from_origin(x, y) - radius


if __name__ == "__main__":
    import doctest
    doctest.testmod()


------------------------------------------------------------------------------------------------------------------------------------------------

FuzzyBool.py

import Util


@Util.complete_comparisons
class FuzzyBool:

    def __init__(self, value=0.0):
        """
        >>> f = FuzzyBool()
        >>> g = FuzzyBool(.5)
        >>> h = FuzzyBool(3.75)
        >>> f, g, h
        (FuzzyBool(0.0), FuzzyBool(0.5), FuzzyBool(0.0))
        """
        self.__value = value if 0.0 <= value <= 1.0 else 0.0


    def __invert__(self):
        """Returns the logical not of this FuzzyBool
        >>> f = FuzzyBool(0.125)
        >>> ~f
        FuzzyBool(0.875)
        >>> ~FuzzyBool()
        FuzzyBool(1.0)
        >>> ~FuzzyBool(1)
        FuzzyBool(0.0)
        """
        return FuzzyBool(1.0 - self.__value)


    def __and__(self, other):
        """Returns the logical and of this FuzzyBool and the other one
        >>> FuzzyBool(0.5) & FuzzyBool(0.6)
        FuzzyBool(0.5)
        """
        return FuzzyBool(min(self.__value, other.__value))


    def __iand__(self, other):
        """Applies logical and to this FuzzyBool with the other one
        >>> f = FuzzyBool(0.5)
        >>> f &= FuzzyBool(0.6)
        >>> f
        FuzzyBool(0.5)
        """
        self.__value = min(self.__value, other.__value)
        return self


    @staticmethod
    def conjunction(*fuzzies):
        """Returns the logical and of all the FuzzyBools
        >>> FuzzyBool.conjunction(FuzzyBool(0.5), FuzzyBool(0.6), 0.2, 0.125)
        FuzzyBool(0.125)
        """
        return FuzzyBool(min([float(x) for x in fuzzies]))


    def __or__(self, other):
        """Returns the logical or of this FuzzyBool and the other one
        >>> FuzzyBool(0.5) | FuzzyBool(0.75)
        FuzzyBool(0.75)
        """
        return FuzzyBool(max(self.__value, other.__value))


    def __ior__(self, other):
        """Applies logical or to this FuzzyBool with the other one
        >>> f = FuzzyBool(0.5)
        >>> f |= FuzzyBool(0.75)
        >>> f
        FuzzyBool(0.75)
        """
        self.__value = max(self.__value, other.__value)
        return self


    @staticmethod
    def disjunction(*fuzzies):
        """Returns the logical or of all the FuzzyBools
        >>> FuzzyBool.disjunction(FuzzyBool(0.5), FuzzyBool(0.75), 0.2, 0.1)
        FuzzyBool(0.75)
        """
        return FuzzyBool(max([float(x) for x in fuzzies]))


    def __repr__(self):
        """
        >>> f = FuzzyBool(0.5)
        >>> repr(f)
        'FuzzyBool(0.5)'
        """
        return ("{0}({1})".format(self.__class__.__name__,
                                  self.__value))


    def __str__(self):
        """
        >>> f = FuzzyBool(0.5)
        >>> str(f)
        '0.5'
        """
        return str(self.__value)


    def __bool__(self):
        """
        >>> f = FuzzyBool(.3)
        >>> g = FuzzyBool(.51)
        >>> bool(f), bool(g)
        (False, True)
        """
        return self.__value > 0.5


    def __int__(self):
        return round(self.__value)


    def __float__(self):
        return self.__value


    def __lt__(self, other):
        return self.__value < other.__value


    def __eq__(self, other):
        return self.__value == other.__value


    def __hash__(self):
        return hash(id(self))


    def __format__(self, format_spec):
        """
        >>> f = FuzzyBool(.875)
        >>> "{0:.0%}".format(f)
        '88%'
        >>> "{0:.1%}".format(f)
        '87.5%'
        """
        return format(self.__value, format_spec)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

-----------------------------------------------------------------------------------------------------------------------------------------------------


"""
Implements an immutable FuzzyBool data type that can only have values in
the interval [0.0, 1.0] and which supports the basic logical operations
not (~), and (&), and or (|) using fuzzy logic.
Tests of inherited methods
>>> f = FuzzyBool()
>>> g = FuzzyBool(.5)
>>> h = FuzzyBool(3.75)
>>> print(f, g, h)
0.0 0.5 0.0
>>> h = ~h
>>> f = FuzzyBool(0.2)
>>> f < g
True
>>> h >= g
True
>>> f + g
Traceback (most recent call last):
...
TypeError: unsupported operand type(s) for +: 'FuzzyBool' and 'FuzzyBool'
>>> -f
Traceback (most recent call last):
...
TypeError: bad operand type for unary -: 'FuzzyBool'
>>> int(h), int(g), int(FuzzyBool(0.51))
(1, 0, 1)
>>> f = FuzzyBool(0.5)
>>> str(f)
'0.5'
"""


def conjunction(*fuzzies):
    """Returns the logical and of all the FuzzyBools
    >>> conjunction(FuzzyBool(0.5), FuzzyBool(0.6), 0.2, 0.125)
    FuzzyBool(0.125)
    """
    return FuzzyBool(min(fuzzies))


def disjunction(*fuzzies):
    """Returns the logical or of all the FuzzyBools
    >>> disjunction(FuzzyBool(0.5), FuzzyBool(0.75), 0.2, 0.1)
    FuzzyBool(0.75)
    """
    return FuzzyBool(max(fuzzies))


class FuzzyBool(float):

    def __new__(cls, value=0.0):
        """
        >>> f = FuzzyBool()
        >>> g = FuzzyBool(.5)
        >>> h = FuzzyBool(3.75)
        >>> f, g, h
        (FuzzyBool(0.0), FuzzyBool(0.5), FuzzyBool(0.0))
        """
        return super().__new__(cls,
                value if 0.0 <= value <= 1.0 else 0.0)


    def __invert__(self):
        """Returns the logical not of this FuzzyBool
        >>> f = FuzzyBool(0.125)
        >>> ~f
        FuzzyBool(0.875)
        >>> ~FuzzyBool()
        FuzzyBool(1.0)
        >>> ~FuzzyBool(1)
        FuzzyBool(0.0)
        """
        return FuzzyBool(1.0 - float(self))


    def __and__(self, other):
        """Returns the logical and of this FuzzyBool and the other one
        >>> FuzzyBool(0.5) & FuzzyBool(0.6)
        FuzzyBool(0.5)
        """
        return FuzzyBool(min(self, other))


    def __iand__(self, other):
        """Applies logical and to this FuzzyBool with the other one
        >>> f = FuzzyBool(0.5)
        >>> f &= FuzzyBool(0.6)
        >>> f
        FuzzyBool(0.5)
        """
        return FuzzyBool(min(self, other))


    def __or__(self, other):
        """Returns the logical or of this FuzzyBool and the other one
        >>> FuzzyBool(0.5) | FuzzyBool(0.75)
        FuzzyBool(0.75)
        """
        return FuzzyBool(max(self, other))


    def __ior__(self, other):
        """Applies logical or to this FuzzyBool with the other one
        >>> f = FuzzyBool(0.5)
        >>> f |= FuzzyBool(0.75)
        >>> f
        FuzzyBool(0.75)
        """
        return FuzzyBool(max(self, other))


    def __repr__(self):
        """
        >>> f = FuzzyBool(0.5)
        >>> repr(f)
        'FuzzyBool(0.5)'
        """
        return ("{0}({1})".format(self.__class__.__name__,
                                  super().__repr__()))


    def __bool__(self):
        """
        >>> f = FuzzyBool(.3)
        >>> g = FuzzyBool(.51)
        >>> bool(f), bool(g)
        (False, True)
        """
        return self > 0.5


    def __int__(self):
        """
        >>> f = FuzzyBool(.3)
        >>> g = FuzzyBool(.51)
        >>> int(f), int(g)
        (0, 1)
        """
        return round(self)


    for name, operator in (("__neg__", "-"),
                           ("__index__", "index()")):
        message = ("bad operand type for unary {0}: '{{self}}'"
                   .format(operator))
        exec("def {0}(self): raise TypeError(\"{1}\".format("
             "self=self.__class__.__name__))".format(name, message))

    for name, operator in (("__xor__", "^"), ("__ixor__", "^="),
            ("__add__", "+"), ("__iadd__", "+="), ("__radd__", "+"),
            ("__sub__", "-"), ("__isub__", "-="), ("__rsub__", "-"),
            ("__mul__", "*"), ("__imul__", "*="), ("__rmul__", "*"),
            ("__pow__", "**"), ("__ipow__", "**="),
            ("__rpow__", "**"), ("__floordiv__", "//"),
            ("__ifloordiv__", "//="), ("__rfloordiv__", "//"),
            ("__truediv__", "/"), ("__itruediv__", "/="),
            ("__rtruediv__", "/"), ("__divmod__", "divmod()"),
            ("__rdivmod__", "divmod()"), ("__mod__", "%"),
            ("__imod__", "%="), ("__rmod__", "%"),
            ("__lshift__", "<<"), ("__ilshift__", "<<="),
            ("__rlshift__", "<<"), ("__rshift__", ">>"),
            ("__irshift__", ">>="), ("__rrshift__", ">>")):
        message = ("unsupported operand type(s) for {0}: "
                   "'{{self}}'{{join}} {{args}}".format(operator))
        exec("def {0}(self, *args):\n"
             "    types = [\"'\" + arg.__class__.__name__ + \"'\" "
             "for arg in args]\n"
             "    raise TypeError(\"{1}\".format("
             "self=self.__class__.__name__, "
             "join=(\" and\" if len(args) == 1 else \",\"),"
             "args=\", \".join(types)))".format(name, message))


if __name__ == "__main__":
    import doctest
    doctest.testmod()

-----------------------------------------------------------------------------------------------------------------------------------------------------
Image.py

"""
This module provides the Image class which holds (x, y, color) triples
and a background color to provide a kind of sparse-array representation of
an image. A method to export the image in XPM format is also provided.
>>> import os
>>> import tempfile
>>> red = "#FF0000"
>>> blue = "#0000FF"
>>> img = os.path.join(tempfile.gettempdir(), "test.img")
>>> xpm = os.path.join(tempfile.gettempdir(), "test.xpm")
>>> image = Image(10, 8, img)
>>> for x, y in ((0, 0), (0, 7), (1, 0), (1, 1), (1, 6), (1, 7), (2, 1),
...             (2, 2), (2, 5), (2, 6), (2, 7), (3, 2), (3, 3), (3, 4),
...             (3, 5), (3, 6), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4),
...             (5, 5), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (7, 1),
...             (7, 2), (7, 5), (7, 6), (7, 7), (8, 0), (8, 1), (8, 6),
...             (8, 7), (9, 0), (9, 7)):
...    image[x, y] = blue
>>> for x, y in ((3, 1), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2),
...             (6, 1)):
...    image[(x, y)] = red
>>> print(image.width, image.height, len(image.colors), image.background)
10 8 3 #FFFFFF
>>> border_color = "#FF0000" # red
>>> square_color = "#0000FF" # blue
>>> width, height = 240, 60
>>> midx, midy = width // 2, height // 2
>>> image = Image(width, height, img, "#F0F0F0")
>>> for x in range(width):
...     for y in range(height):
...         if x < 5 or x >= width - 5 or y < 5 or y >= height -5:
...             image[x, y] = border_color
...         elif midx - 20 < x < midx + 20 and midy - 20 < y < midy + 20:
...             image[x, y] = square_color
>>> print(image.width, image.height, len(image.colors), image.background)
240 60 3 #F0F0F0
>>> image.save()
>>> newimage = Image(1, 1, img)
>>> newimage.load()
>>> print(newimage.width, newimage.height, len(newimage.colors), newimage.background)
240 60 3 #F0F0F0
>>> image.export(xpm)
>>> image.thing
Traceback (most recent call last):
...
AttributeError: 'Image' object has no attribute 'thing'
>>> for name in (img, xpm):
...     try:
...         os.remove(name)
...     except EnvironmentError:
...         pass
"""

import os
import pickle

USE_GETATTR = False


class ImageError(Exception): pass
class CoordinateError(ImageError): pass
class LoadError(ImageError): pass
class SaveError(ImageError): pass
class ExportError(ImageError): pass
class NoFilenameError(ImageError): pass


class Image:

    def __init__(self, width, height, filename="",
                 background="#FFFFFF"):
        """An image represented as HTML-style color values
        (color names or hex strings) at (x, y) coordinates with any
        unspecified points assumed to be the background
        """
        self.filename = filename
        self.__background = background
        self.__data = {}
        self.__width = width
        self.__height = height
        self.__colors = {self.__background}


    if USE_GETATTR:
        def __getattr__(self, name):
            """
            >>> image = Image(10, 10)
            >>> len(image.colors) == 1
            True
            >>> image.width == image.height == 10
            True
            >>> image.thing
            Traceback (most recent call last):
            ...
            AttributeError: 'Image' object has no attribute 'thing'
            """
            if name == "colors":
                return set(self.__colors)
            classname = self.__class__.__name__
            if name in frozenset({"background", "width", "height"}):
                return self.__dict__["_{classname}__{name}".format(
                        **locals())]
            raise AttributeError("'{classname}' object has no "
                    "attribute '{name}'".format(**locals()))
    else:
        @property
        def background(self):
            return self.__background


        @property
        def width(self):
            return self.__width


        @property
        def height(self):
            return self.__height


        @property
        def colors(self):
            return set(self.__colors)


    def __getitem__(self, coordinate):
        """Returns the color at the given (x, y) coordinate; this will
        be the background color if the color has never been set
        """
        assert len(coordinate) == 2, "coordinate should be a 2-tuple"
        if (not (0 <= coordinate[0] < self.width) or
            not (0 <= coordinate[1] < self.height)):
            raise CoordinateError(str(coordinate))
        return self.__data.get(tuple(coordinate), self.__background)


    def __setitem__(self, coordinate, color):
        """Sets the color at the given (x, y), coordinate
        """
        assert len(coordinate) == 2, "coordinate should be a 2-tuple"
        if (not (0 <= coordinate[0] < self.width) or
            not (0 <= coordinate[1] < self.height)):
            raise CoordinateError(str(coordinate))
        if color == self.__background:
            self.__data.pop(tuple(coordinate), None)
        else:
            self.__data[tuple(coordinate)] = color
            self.__colors.add(color)


    def __delitem__(self, coordinate):
        """Deletes the color at the given (x, y) coordinate
        In effect this makes the coordinate's color the background color.
        """
        assert len(coordinate) == 2, "coordinate should be a 2-tuple"
        if (not (0 <= coordinate[0] < self.width) or
            not (0 <= coordinate[1] < self.height)):
            raise CoordinateError(str(coordinate))
        self.__data.pop(tuple(coordinate), None)


    def save(self, filename=None):
        """Saves the current image, or the one specified by filename
        If filename is specified the internal filename is set to it.
        """
        if filename is not None:
            self.filename = filename
        if not self.filename:
            raise NoFilenameError()

        fh = None
        try:
            data = [self.width, self.height, self.__background,
                    self.__data]
            fh = open(self.filename, "wb")
            pickle.dump(data, fh, pickle.HIGHEST_PROTOCOL)
        except (EnvironmentError, pickle.PicklingError) as err:
            raise SaveError(str(err))
        finally:
            if fh is not None:
                fh.close()

        
    def load(self, filename=None):
        """Loads the current image, or the one specified by filename
        If filename is specified the internal filename is set to it.
        """
        if filename is not None:
            self.filename = filename
        if not self.filename:
            raise NoFilenameError()

        fh = None
        try:
            fh = open(self.filename, "rb")
            data = pickle.load(fh)
            (self.__width, self.__height, self.__background,
             self.__data) = data
            self.__colors = (set(self.__data.values()) |
                             {self.__background})
        except (EnvironmentError, pickle.UnpicklingError) as err:
            raise LoadError(str(err))
        finally:
            if fh is not None:
                fh.close()


    def export(self, filename):
        """Exports the image to the specified filename
        """
        if filename.lower().endswith(".xpm"):
            self.__export_xpm(filename)
        else:
            raise ExportError("unsupported export format: " +
                              os.path.splitext(filename)[1])


    def __export_xpm(self, filename):
        """Exports the image as an XPM file if less than 8930 colors are
        used
        """
        name = os.path.splitext(os.path.basename(filename))[0]
        count = len(self.__colors)
        chars = [chr(x) for x in range(32, 127) if chr(x) != '"']
        if count > len(chars):
            chars = []
            for x in range(32, 127):
                if chr(x) == '"':
                    continue
                for y in range(32, 127):
                    if chr(y) == '"':
                        continue
                    chars.append(chr(x) + chr(y))
        chars.reverse()
        if count > len(chars):
            raise ExportError("cannot export XPM: too many colors")
        fh = None
        try:
            fh = open(filename, "w", encoding="ascii")
            fh.write("/* XPM */\n")
            fh.write("static char *{0}[] = {{\n".format(name))
            fh.write("/* columns rows colors chars-per-pixel */\n")
            fh.write('"{0.width} {0.height} {1} {2}",\n'.format(
                     self, count, len(chars[0])))
            char_for_colour = {}
            for color in self.__colors:
                char = chars.pop()
                fh.write('"{char} c {color}",\n'.format(**locals()))
                char_for_colour[color] = char
            fh.write("/* pixels */\n")
            for y in range(self.height):
                row = []
                for x in range(self.width):
                    color = self.__data.get((x, y), self.__background)
                    row.append(char_for_colour[color])
                fh.write('"{0}",\n'.format("".join(row)))
            fh.write("};\n")
        except EnvironmentError as err:
            raise ExportError(str(err))
        finally:
            if fh is not None:
                fh.close()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
-----------------------------------------------------------------------------------------------------------------------------------------------------

Image_ans.py
import os
import pickle

USE_GETATTR = False


class ImageError(Exception): pass
class CoordinateError(ImageError): pass
class LoadError(ImageError): pass
class SaveError(ImageError): pass
class ExportError(ImageError): pass
class NoFilenameError(ImageError): pass


class Image:

    def __init__(self, width, height, filename="",
                 background="#FFFFFF"):
        """An image represented as HTML-style color values
        (color names or hex strings) at (x, y) coordinates with any
        unspecified points assumed to be the background
        """
        self.filename = filename
        self.__background = background
        self.__data = {}
        self.__width = width
        self.__height = height
        self.__colors = {self.__background}


    if USE_GETATTR:
        def __getattr__(self, name):
            """
            >>> image = Image(10, 10)
            >>> len(image.colors) == 1
            True
            >>> image.width == image.height == 10
            True
            >>> image.thing
            Traceback (most recent call last):
            ...
            AttributeError: 'Image' object has no attribute 'thing'
            """
            if name == "colors":
                return set(self.__colors)
            classname = self.__class__.__name__
            if name in frozenset({"background", "width", "height"}):
                return self.__dict__["_{classname}__{name}".format(
                        **locals())]
            raise AttributeError("'{classname}' object has no "
                    "attribute '{name}'".format(**locals()))
    else:
        @property
        def background(self):
            return self.__background


        @property
        def width(self):
            return self.__width


        @property
        def height(self):
            return self.__height


        @property
        def colors(self):
            return set(self.__colors)


    def __getitem__(self, coordinate):
        """Returns the color at the given (x, y) coordinate; this will
        be the background color if the color has never been set
        """
        assert len(coordinate) == 2, "coordinate should be a 2-tuple"
        if (not (0 <= coordinate[0] < self.width) or
            not (0 <= coordinate[1] < self.height)):
            raise CoordinateError(str(coordinate))
        return self.__data.get(tuple(coordinate), self.__background)


    def __setitem__(self, coordinate, color):
        """Sets the color at the given (x, y), coordinate
        """
        assert len(coordinate) == 2, "coordinate should be a 2-tuple"
        if (not (0 <= coordinate[0] < self.width) or
            not (0 <= coordinate[1] < self.height)):
            raise CoordinateError(str(coordinate))
        if color == self.__background:
            self.__data.pop(tuple(coordinate), None)
        else:
            self.__data[tuple(coordinate)] = color
            self.__colors.add(color)


    def __delitem__(self, coordinate):
        """Deletes the color at the given (x, y) coordinate
        In effect this makes the coordinate's color the background color.
        """
        assert len(coordinate) == 2, "coordinate should be a 2-tuple"
        if (not (0 <= coordinate[0] < self.width) or
            not (0 <= coordinate[1] < self.height)):
            raise CoordinateError(str(coordinate))
        self.__data.pop(tuple(coordinate), None)


    def resize(self, width=None, height=None):
        """Resizes to the given dimensions; returns True if changes made
        If a dimension is None; keeps the original. Deletes all out of
        range points.
        >>> image = Image(10, 10)
        >>> for x, y in zip(range(10), range(10)):
        ...     image[x, y] = "#00FF00" if x < 5 else "#0000FF"
        >>> image.width, image.height, len(image.colors)
        (10, 10, 3)
        >>> image.resize(5, 5)
        True
        >>> image.width, image.height, len(image.colors)
        (5, 5, 2)
        """
        if width is None and height is None:
            return False
        if width is None:
            width = self.width
        if height is None:
            height = self.height
        if width >= self.width and height >= self.height:
            self.__width = width
            self.__height = height
            return True
        self.__width = width
        self.__height = height
        for x, y in list(self.__data.keys()):
            if x >= self.width or y >= self.height:
                del self.__data[(x, y)]
        self.__colors = set(self.__data.values()) | {self.__background}
        return True


    def save(self, filename=None):
        """Saves the current image, or the one specified by filename
        If filename is specified the internal filename is set to it.
        """
        if filename is not None:
            self.filename = filename
        if not self.filename:
            raise NoFilenameError()

        fh = None
        try:
            data = [self.width, self.height, self.__background,
                    self.__data]
            fh = open(self.filename, "wb")
            pickle.dump(data, fh, pickle.HIGHEST_PROTOCOL)
        except (EnvironmentError, pickle.PicklingError) as err:
            raise SaveError(str(err))
        finally:
            if fh is not None:
                fh.close()

        
    def load(self, filename=None):
        """Loads the current image, or the one specified by filename
        If filename is specified the internal filename is set to it.
        """
        if filename is not None:
            self.filename = filename
        if not self.filename:
            raise NoFilenameError()

        fh = None
        try:
            fh = open(self.filename, "rb")
            data = pickle.load(fh)
            (self.__width, self.__height, self.__background,
             self.__data) = data
            self.__colors = (set(self.__data.values()) |
                             {self.__background})
        except (EnvironmentError, pickle.UnpicklingError) as err:
            raise LoadError(str(err))
        finally:
            if fh is not None:
                fh.close()


    def export(self, filename):
        """Exports the image to the specified filename
        """
        if filename.lower().endswith(".xpm"):
            self.__export_xpm(filename)
        else:
            raise ExportError("unsupported export format: " +
                              os.path.splitext(filename)[1])


    def __export_xpm(self, filename):
        """Exports the image as an XPM file if less than 8930 colors are
        used
        """
        name = os.path.splitext(os.path.basename(filename))[0]
        count = len(self.__colors)
        chars = [chr(x) for x in range(32, 127) if chr(x) != '"']
        if count > len(chars):
            chars = []
            for x in range(32, 127):
                if chr(x) == '"':
                    continue
                for y in range(32, 127):
                    if chr(y) == '"':
                        continue
                    chars.append(chr(x) + chr(y))
        chars.reverse()
        if count > len(chars):
            raise ExportError("cannot export XPM: too many colors")
        fh = None
        try:
            fh = open(filename, "w", encoding="ascii")
            fh.write("/* XPM */\n")
            fh.write("static char *{0}[] = {{\n".format(name))
            fh.write("/* columns rows colors chars-per-pixel */\n")
            fh.write('"{0.width} {0.height} {1} {2}",\n'.format(
                     self, count, len(chars[0])))
            char_for_colour = {}
            for color in self.__colors:
                char = chars.pop()
                fh.write('"{char} c {color}",\n'.format(**locals()))
                char_for_colour[color] = char
            fh.write("/* pixels */\n")
            for y in range(self.height):
                row = []
                for x in range(self.width):
                    color = self.__data.get((x, y), self.__background)
                    row.append(char_for_colour[color])
                fh.write('"{0}",\n'.format("".join(row)))
            fh.write("};\n")
        except EnvironmentError as err:
            raise ExportError(str(err))
        finally:
            if fh is not None:
                fh.close()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
-----------------------------------------------------------------------------------------------------------------------------------------------------
Shape.py
his module provides the Point and Circle classes.
>>> point = Point()
>>> point
Point(0, 0)
>>> point.x = 12
>>> str(point)
'(12, 0)'
>>> a = Point(3, 4)
>>> b = Point(3, 4)
>>> a == b
True
>>> a == point
False
>>> a != point
True
>>> circle = Circle(2)
>>> circle
Circle(2, 0, 0)
>>> circle.radius = 3
>>> circle.x = 12
>>> circle
Circle(3, 12, 0)
>>> a = Circle(4, 5, 6)
>>> b = Circle(4, 5, 6)
>>> a == b
True
>>> a == circle
False
>>> a != circle
True
"""

import math


class Point:

    def __init__(self, x=0, y=0):
        """A 2D cartesian coordinate
        >>> point = Point()
        >>> point
        Point(0, 0)
        """
        self.x = x
        self.y = y


    def distance_from_origin(self):
        """Returns the distance of the point from the origin
        >>> point = Point(3, 4)
        >>> point.distance_from_origin()
        5.0
        """
        return math.hypot(self.x, self.y)


    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


    def __repr__(self):
        return "Point({0.x!r}, {0.y!r})".format(self)


    def __str__(self):
        return "({0.x!r}, {0.y!r})".format(self)


class Circle(Point):

    def __init__(self, radius, x=0, y=0):
        """A Circle
        >>> circle = Circle(2)
        >>> circle
        Circle(2, 0, 0)
        """
        super().__init__(x, y)
        self.radius = radius


    def edge_distance_from_origin(self):
        """The distance of the circle's edge from the origin
        >>> circle = Circle(2, 3, 4)
        >>> circle.edge_distance_from_origin()
        3.0
        """
        return abs(self.distance_from_origin() - self.radius)


    def area(self):
        """The circle's area
        >>> circle = Circle(3)
        >>> a = circle.area()
        >>> int(a)
        28
        """
        return math.pi * (self.radius ** 2)


    def circumference(self):
        """The circle's circumference
        >>> circle = Circle(3)
        >>> d = circle.circumference()
        >>> int(d)
        18
        """
        return 2 * math.pi * self.radius


    def __eq__(self, other):
        return self.radius == other.radius and super().__eq__(other)


    def __repr__(self):
        return "Circle({0.radius!r}, {0.x!r}, {0.y!r})".format(self)


    def __str__(self):
        return repr(self)
        

if __name__ == "__main__":
    import doctest
    doctest.testmod()
-----------------------------------------------------------------------------------------------------------------------------------------------------

 Shape_ans.py

>>> point = Point()
>>> point
Point(0, 0)
>>> point.x = 12
>>> str(point)
'(12, 0)'
>>> a = Point(3, 4)
>>> b = Point(3, 4)
>>> a == b
True
>>> a == point
False
>>> a != point
True
>>> circle = Circle(2)
>>> circle
Circle(2, 0, 0)
>>> circle.radius = 3
>>> circle.x = 12
>>> circle
Circle(3, 12, 0)
>>> a = Circle(4, 5, 6)
>>> b = Circle(4, 5, 6)
>>> a == b
True
>>> a == circle
False
>>> a != circle
True
"""

import math


class Point:

    def __init__(self, x=0, y=0):
        """A 2D cartesian coordinate
        >>> point = Point()
        >>> point
        Point(0, 0)
        """
        self.x = x
        self.y = y


    def distance_from_origin(self):
        """Returns the distance of the point from the origin
        >>> point = Point(3, 4)
        >>> point.distance_from_origin()
        5.0
        """
        return math.hypot(self.x, self.y)


    def __add__(self, other):
        """Returns a new Point whose coordinate are the sum of this
        one's and the other one's
        >>> p = Point(2, 4)
        >>> q = p + Point(3, 5)
        >>> q
        Point(5, 9)
        """
        return Point(self.x + other.x, self.y + other.y)


    def __iadd__(self, other):
        """Returns this Point with its coordinate set to the sum of this
        one's and the other one's
        >>> p = Point(2, 4)
        >>> p += Point(3, 5)
        >>> p
        Point(5, 9)
        """
        self.x += other.x
        self.y += other.y
        return self


    def __sub__(self, other):
        """Returns a new Point whose coordinate are the difference of this
        one's and the other one's
        >>> p = Point(2, 4)
        >>> q = p - Point(3, 5)
        >>> q
        Point(-1, -1)
        """
        return Point(self.x - other.x, self.y - other.y)


    def __isub__(self, other):
        """Returns this Point with its coordinate set to the difference
        of this one's and the other one's
        >>> p = Point(2, 4)
        >>> p -= Point(3, 5)
        >>> p
        Point(-1, -1)
        """
        self.x -= other.x
        self.y -= other.y
        return self


    def __mul__(self, other):
        """Returns a new Point whose coordinate is this one's multiplied
        by the other number
        >>> p = Point(2, 4)
        >>> q = p * 3
        >>> q
        Point(6, 12)
        """
        return Point(self.x * other, self.y * other)


    def __imul__(self, other):
        """Returns this Point with its coordinate set to this one's
        multiplied by the other number
        >>> p = Point(2, 4)
        >>> p *= 3
        >>> p
        Point(6, 12)
        """
        self.x *= other
        self.y *= other
        return self


    def __truediv__(self, other):
        """Returns a new Point whose coordinate is this one's divided
        by the other number
        >>> p = Point(2, 4)
        >>> q = p / 2
        >>> q
        Point(1.0, 2.0)
        """
        return Point(self.x / other, self.y / other)


    def __itruediv__(self, other):
        """Returns this Point with its coordinate set to this one's
        divided by the other number
        >>> p = Point(2, 4)
        >>> p /= 2
        >>> p
        Point(1.0, 2.0)
        """
        self.x /= other
        self.y /= other
        return self


    def __floordiv__(self, other):
        """Returns a new Point whose coordinate is this one's floor
        divided by the other number
        >>> p = Point(2, 4)
        >>> q = p // 2
        >>> q
        Point(1, 2)
        """
        return Point(self.x // other, self.y // other)


    def __ifloordiv__(self, other):
        """Returns this Point with its coordinate set to this one's
        floor divided by the other number
        >>> p = Point(2, 4)
        >>> p //= 2
        >>> p
        Point(1, 2)
        """
        self.x //= other
        self.y //= other
        return self


    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


    def __repr__(self):
        return "Point({0.x!r}, {0.y!r})".format(self)


    def __str__(self):
        return "({0.x!r}, {0.y!r})".format(self)


class Circle(Point):

    def __init__(self, radius, x=0, y=0):
        """A Circle
        >>> circle = Circle(2)
        >>> circle
        Circle(2, 0, 0)
        """
        super().__init__(x, y)
        self.radius = radius


    def edge_distance_from_origin(self):
        """The distance of the circle's edge from the origin
        >>> circle = Circle(2, 3, 4)
        >>> circle.edge_distance_from_origin()
        3.0
        """
        return abs(self.distance_from_origin() - self.radius)


    def area(self):
        """The circle's area
        >>> circle = Circle(3)
        >>> a = circle.area()
        >>> int(a)
        28
        """
        return math.pi * (self.radius ** 2)


    def circumference(self):
        """The circle's circumference
        >>> circle = Circle(3)
        >>> d = circle.circumference()
        >>> int(d)
        18
        """
        return 2 * math.pi * self.radius


    def __eq__(self, other):
        return self.radius == other.radius and super().__eq__(other)


    def __repr__(self):
        return "Circle({0.radius!r}, {0.x!r}, {0.y!r})".format(self)


    def __str__(self):
        return repr(self)
        

if __name__ == "__main__":
    import doctest
    doctest.testmod()
-----------------------------------------------------------------------------------------------------------------------------------------------------
ShapeAlt.py

>>> point = Point()
>>> point
Point(0, 0)
>>> point.x = 12
>>> str(point)
'(12, 0)'
>>> a = Point(3, 4)
>>> b = Point(3, 4)
>>> a == b
True
>>> a == point
False
>>> a != point
True
>>> circle = Circle(2)
>>> circle
Circle(2, 0, 0)
>>> circle.radius = 3
>>> circle.x = 12
>>> circle
Circle(3, 12, 0)
>>> a = Circle(4, 5, 6)
>>> b = Circle(4, 5, 6)
>>> a == b
True
>>> a == circle
False
>>> a != circle
True
"""

import math


class Point:

    def __init__(self, x=0, y=0):
        """A 2D cartesian coordinate
        >>> point = Point()
        >>> point
        Point(0, 0)
        """
        self.x = x
        self.y = y


    @property
    def distance_from_origin(self):
        """The distance of the point from the origin
        >>> point = Point(3, 4)
        >>> point.distance_from_origin
        5.0
        """
        return math.hypot(self.x, self.y)


    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


    def __repr__(self):
        return ("{0.__class__.__name__}({0.x!r}, {0.y!r})".format(
                self))


    def __str__(self):
        return "({0.x!r}, {0.y!r})".format(self)


class Circle(Point):

    def __init__(self, radius, x=0, y=0):
        """A Circle
        >>> circle = Circle(2)
        >>> circle
        Circle(2, 0, 0)
        """
        super().__init__(x, y)
        self.radius = radius


    @property
    def area(self):
        """The circle's area
        >>> circle = Circle(3)
        >>> a = circle.area
        >>> int(a)
        28
        """
        return math.pi * (self.radius ** 2)


    @property
    def edge_distance_from_origin(self):
        """The distance of the circle's edge from the origin
        >>> circle = Circle(2, 3, 4)
        >>> circle.edge_distance_from_origin
        3.0
        """
        return abs(self.distance_from_origin - self.radius)


    @property
    def circumference(self):
        """The circle's circumference
        >>> circle = Circle(3)
        >>> d = circle.circumference
        >>> int(d)
        18
        """
        return 2 * math.pi * self.radius


    @property
    def radius(self):
        """The circle's radius
        >>> circle = Circle(-2)
        Traceback (most recent call last):
        ...
        AssertionError: radius must be nonzero and non-negative
        >>> circle = Circle(4)
        >>> circle.radius = -1
        Traceback (most recent call last):
        ...
        AssertionError: radius must be nonzero and non-negative
        >>> circle.radius = 6
        """
        return self.__radius

    @radius.setter
    def radius(self, radius):
        assert radius > 0, "radius must be nonzero and non-negative"
        self.__radius = radius


    def __eq__(self, other):
        return self.radius == other.radius and super().__eq__(other)


    def __repr__(self):
        return ("{0.__class__.__name__}({0.radius!r}, {0.x!r}, "
                "{0.y!r})".format(self))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
-----------------------------------------------------------------------------------------------------------------------------------------------------
ShapeAlt_ans.py

>>> point = Point()
>>> point
Point(0, 0)
>>> point.x = 12
>>> str(point)
'(12, 0)'
>>> a = Point(3, 4)
>>> b = Point(3, 4)
>>> a == b
True
>>> a == point
False
>>> a != point
True
>>> circle = Circle(2)
>>> circle
Circle(2, 0, 0)
>>> circle.radius = 3
>>> circle.x = 12
>>> circle
Circle(3, 12, 0)
>>> a = Circle(4, 5, 6)
>>> b = Circle(4, 5, 6)
>>> a == b
True
>>> a == circle
False
>>> a != circle
True
"""

import math


class Point:

    def __init__(self, x=0, y=0):
        """A 2D cartesian coordinate
        >>> point = Point()
        >>> point
        Point(0, 0)
        """
        self.x = x
        self.y = y


    @property
    def distance_from_origin(self):
        """The distance of the point from the origin
        >>> point = Point(3, 4)
        >>> point.distance_from_origin
        5.0
        """
        return math.hypot(self.x, self.y)


    def __add__(self, other):
        """Returns a new Point whose coordinate are the sum of this
        one's and the other one's
        >>> p = Point(2, 4)
        >>> q = p + Point(3, 5)
        >>> q
        Point(5, 9)
        """
        return Point(self.x + other.x, self.y + other.y)


    def __iadd__(self, other):
        """Returns this Point with its coordinate set to the sum of this
        one's and the other one's
        >>> p = Point(2, 4)
        >>> p += Point(3, 5)
        >>> p
        Point(5, 9)
        """
        self.x += other.x
        self.y += other.y
        return self


    def __sub__(self, other):
        """Returns a new Point whose coordinate are the difference of this
        one's and the other one's
        >>> p = Point(2, 4)
        >>> q = p - Point(3, 5)
        >>> q
        Point(-1, -1)
        """
        return Point(self.x - other.x, self.y - other.y)


    def __isub__(self, other):
        """Returns this Point with its coordinate set to the difference
        of this one's and the other one's
        >>> p = Point(2, 4)
        >>> p -= Point(3, 5)
        >>> p
        Point(-1, -1)
        """
        self.x -= other.x
        self.y -= other.y
        return self


    def __mul__(self, other):
        """Returns a new Point whose coordinate is this one's multiplied
        by the other number
        >>> p = Point(2, 4)
        >>> q = p * 3
        >>> q
        Point(6, 12)
        """
        return Point(self.x * other, self.y * other)


    def __imul__(self, other):
        """Returns this Point with its coordinate set to this one's
        multiplied by the other number
        >>> p = Point(2, 4)
        >>> p *= 3
        >>> p
        Point(6, 12)
        """
        self.x *= other
        self.y *= other
        return self


    def __truediv__(self, other):
        """Returns a new Point whose coordinate is this one's divided
        by the other number
        >>> p = Point(2, 4)
        >>> q = p / 2
        >>> q
        Point(1.0, 2.0)
        """
        return Point(self.x / other, self.y / other)


    def __itruediv__(self, other):
        """Returns this Point with its coordinate set to this one's
        divided by the other number
        >>> p = Point(2, 4)
        >>> p /= 2
        >>> p
        Point(1.0, 2.0)
        """
        self.x /= other
        self.y /= other
        return self


    def __floordiv__(self, other):
        """Returns a new Point whose coordinate is this one's floor
        divided by the other number
        >>> p = Point(2, 4)
        >>> q = p // 2
        >>> q
        Point(1, 2)
        """
        return Point(self.x // other, self.y // other)


    def __ifloordiv__(self, other):
        """Returns this Point with its coordinate set to this one's
        floor divided by the other number
        >>> p = Point(2, 4)
        >>> p //= 2
        >>> p
        Point(1, 2)
        """
        self.x //= other
        self.y //= other
        return self


    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


    def __repr__(self):
        return ("{0.__class__.__name__}({0.x!r}, {0.y!r})".format(
                self))


    def __str__(self):
        return "({0.x!r}, {0.y!r})".format(self)


class Circle(Point):

    def __init__(self, radius, x=0, y=0):
        """A Circle
        >>> circle = Circle(2)
        >>> circle
        Circle(2, 0, 0)
        """
        super().__init__(x, y)
        self.radius = radius


    @property
    def area(self):
        """The circle's area
        >>> circle = Circle(3)
        >>> a = circle.area
        >>> int(a)
        28
        """
        return math.pi * (self.radius ** 2)


    @property
    def edge_distance_from_origin(self):
        """The distance of the circle's edge from the origin
        >>> circle = Circle(2, 3, 4)
        >>> circle.edge_distance_from_origin
        3.0
        """
        return abs(self.distance_from_origin - self.radius)


    @property
    def circumference(self):
        """The circle's circumference
        >>> circle = Circle(3)
        >>> d = circle.circumference
        >>> int(d)
        18
        """
        return 2 * math.pi * self.radius


    @property
    def radius(self):
        """
        The circle's radius
        >>> circle = Circle(-2)
        Traceback (most recent call last):
        ...
        AssertionError: radius must be nonzero and non-negative
        >>> circle = Circle(4)
        >>> circle.radius = -1
        Traceback (most recent call last):
        ...
        AssertionError: radius must be nonzero and non-negative
        >>> circle.radius = 6
        """
        return self.__radius

    @radius.setter
    def radius(self, radius):
        assert radius > 0, "radius must be nonzero and non-negative"
        self.__radius = radius


    def __eq__(self, other):
        return self.radius == other.radius and super().__eq__(other)


    def __repr__(self):
        return ("{0.__class__.__name__}({0.radius!r}, {0.x!r}, "
                "{0.y!r})".format(self))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
-----------------------------------------------------------------------------------------------------------------------------------------------------

 SortedDict.py

hese are tests for inherited methods that aren't reimplemented
>>> d = SortedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
>>> d["i"]
4
>>> d["y"]
6
>>> d["z"]
Traceback (most recent call last):
...
KeyError: 'z'
>>> d = SortedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
>>> d.get("X", 21)
21
>>> d.get("i")
4
>>> d = SortedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
>>> "a" in d
True
>>> "x" in d
False
>>> d = SortedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
>>> len(d)
6
>>> del d["n"]
>>> del d["y"]
>>> len(d)
4
>>> d.clear()
>>> len(d)
0
>>> d = SortedDict(dict(V=1, E=2, I=3, N=4, S=5))
>>> str(d)
"{'E': 2, 'I': 3, 'N': 4, 'S': 5, 'V': 1}"
"""

import SortedList


class SortedDict(dict):

    def __init__(self, dictionary=None, key=None, **kwargs):
        """Initializes with a shallow copy of the given dictionary
        and/or with keyword key=value pairs and preserving order using
        the key function. All keys must be unique.
        key is a key function which defaults to the identity
        function if it is not specified
        >>> d = SortedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> list(d.items())
        [('a', 2), ('i', 4), ('n', 3), ('s', 1), ('t', 5), ('y', 6)]
        >>> dict(SortedDict())
        {}
        >>> e = SortedDict(d)
        >>> list(e.items())
        [('a', 2), ('i', 4), ('n', 3), ('s', 1), ('t', 5), ('y', 6)]
        >>> dict(e)
        {'a': 2, 'i': 4, 's': 1, 't': 5, 'y': 6, 'n': 3}
        >>> f = SortedDict(key=str.lower, S=1, a=2, n=3, I=4, T=5, y=6)
        >>> dict(f)
        {'a': 2, 'I': 4, 'S': 1, 'T': 5, 'y': 6, 'n': 3}
        """
        dictionary = dictionary or {}
        super().__init__(dictionary)
        if kwargs:
            super().update(kwargs)
        self.__keys = SortedList.SortedList(super().keys(), key)


    def update(self, dictionary=None, **kwargs):
        """Updates this dictionary with another dictionary and/or with
        keyword key=value pairs and preserving order using this
        dictionary's key function
        >>> d = SortedDict(dict(s=1, a=2, n=3, i=4, t=5))
        >>> d.update(dict(a=4, z=-4))
        >>> list(d.items())
        [('a', 4), ('i', 4), ('n', 3), ('s', 1), ('t', 5), ('z', -4)]
        >>> del d["a"]
        >>> del d["i"]
        >>> d.update({'g': 9}, a=1, z=3)
        >>> list(d.items())
        [('a', 1), ('g', 9), ('n', 3), ('s', 1), ('t', 5), ('z', 3)]
        >>> e = SortedDict(dict(p=4, q=5))
        >>> del d["a"]
        >>> del d["n"]
        >>> e.update(d)
        >>> list(e.items())
        [('g', 9), ('p', 4), ('q', 5), ('s', 1), ('t', 5), ('z', 3)]
        >>> del d["s"]
        >>> del d["z"]
        >>> d.update(e)
        >>> list(d.items())
        [('g', 9), ('p', 4), ('q', 5), ('s', 1), ('t', 5), ('z', 3)]
        """
        if dictionary is None:
            pass
        elif isinstance(dictionary, dict):
            super().update(dictionary)
        else:
            for key, value in dictionary.items():
                super().__setitem__(key, value)
        if kwargs:
            super().update(kwargs)
        self.__keys = SortedList.SortedList(super().keys(),
                                            self.__keys.key)

    @classmethod
    def fromkeys(cls, iterable, value=None, key=None):
        """A class method that returns a SortedDict whose keys are
        from the iterable and each of whose values is value
        >>> d = SortedDict()
        >>> e = d.fromkeys("KYLIE", 21)
        >>> list(e.items())
        [('E', 21), ('I', 21), ('K', 21), ('L', 21), ('Y', 21)]
        >>> e = SortedDict.fromkeys("KYLIE", 21)
        >>> list(e.items())
        [('E', 21), ('I', 21), ('K', 21), ('L', 21), ('Y', 21)]
        """
        return cls({k: value for k in iterable}, key)


    def value_at(self, index):
        """Returns the index-th item's value
        >>> d = SortedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.value_at(0)
        2
        >>> d.value_at(5)
        6
        >>> d.value_at(2)
        3
        >>> d.value_at(19)
        Traceback (most recent call last):
        ...
        IndexError: list index out of range
        """
        return self[self.__keys[index]]


    def set_value_at(self, index, value):
        """Sets the index-th item's value to the given value
        >>> d = SortedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.value_at(5)
        6
        >>> d.set_value_at(5, 99)
        >>> d.value_at(5)
        99
        >>> d.set_value_at(19, 42)
        Traceback (most recent call last):
        ...
        IndexError: list index out of range
        """
        self[self.__keys[index]] = value


    def clear(self):
        """Removes every item from this SortedDict
        >>> d = SortedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> len(d)
        6
        >>> d.clear()
        >>> len(d)
        0
        >>> d["m"] = 3
        >>> d["a"] = 5
        >>> d["z"] = 7
        >>> d["e"] = 9
        >>> list(d.keys())
        ['a', 'e', 'm', 'z']
        """
        super().clear()
        self.__keys.clear()


    def setdefault(self, key, value=None):
        """If key is in the dictionary, returns its value;
        otherwise adds the key with the given value which is also
        returned
        >>> d = SortedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.setdefault("n", 99)
        3
        >>> list(d.values())
        [2, 4, 3, 1, 5, 6]
        >>> d.setdefault("r", -20)
        -20
        >>> list(d.items())[2:]
        [('n', 3), ('r', -20), ('s', 1), ('t', 5), ('y', 6)]
        >>> d.setdefault("@", -11)
        -11
        >>> d.setdefault("z", 99)
        99
        >>> d.setdefault("m", 50)
        50
        >>> list(d.keys())
        ['@', 'a', 'i', 'm', 'n', 'r', 's', 't', 'y', 'z']
        """
        if key not in self:
            self.__keys.add(key)
        return super().setdefault(key, value)


    def pop(self, key, *args):
        """If key is in the dictionary, returns its value and removes it
        from the dictionary. Otherwise returns arg if specified, or
        raises KeyError if there is no arg.
        >>> d = SortedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.pop("n")
        3
        >>> "n" in d
        False
        >>> d.pop("q", 41)
        41
        >>> list(d.keys())
        ['a', 'i', 's', 't', 'y']
        >>> d.pop("a")
        2
        >>> d.pop("t")
        5
        >>> list(d.keys())
        ['i', 's', 'y']
        >>> d.pop("X")
        Traceback (most recent call last):
        ...
        KeyError: 'X'
        >>> d.pop("X", None)
        >>> d.pop("X", 1)
        1
        """
        if key not in self:
            if len(args) == 0:
                raise KeyError(key)
            return args[0]
        self.__keys.remove(key)
        return super().pop(key, args)


    def popitem(self):
        """Returns and removes an arbitrary item from the dictionary
        >>> d = SortedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> len(d)
        6
        >>> item = d.popitem()
        >>> item = d.popitem()
        >>> item = d.popitem()
        >>> len(d)
        3
        """
        item = super().popitem()
        self.__keys.remove(item[0])
        return item


    def values(self):
        """Returns the dictionary's values in key order
        >>> d = SortedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> list(d.values())
        [2, 4, 3, 1, 5, 6]
        """
        for key in self.__keys:
            yield self[key]


    def items(self):
        """Returns the dictionary's items in key order
        >>> d = SortedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> list(d.items())
        [('a', 2), ('i', 4), ('n', 3), ('s', 1), ('t', 5), ('y', 6)]
        """
        for key in self.__keys:
            yield (key, self[key])


    def __iter__(self):
        """Returns an iterator over the dictionary's keys
        >>> d = SortedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> list(d)
        ['a', 'i', 'n', 's', 't', 'y']
        >>> list(d.keys())
        ['a', 'i', 'n', 's', 't', 'y']
        """
        return iter(self.__keys)

    keys = __iter__


    def __delitem__(self, key):
        """Deletes the item with the given key from the dictionary
        >>> d = SortedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> del d["s"]
        >>> del d["y"]
        >>> del d["a"]
        >>> list(d.keys())
        ['i', 'n', 't']
        >>> del d["X"]
        Traceback (most recent call last):
        ...
        KeyError: 'X'
        >>> d = SortedDict(dict(a=1, b=2, z=3))
        >>> list(d.keys())
        ['a', 'b', 'z']
        >>> del d["c"]
        Traceback (most recent call last):
        ...
        KeyError: 'c'
        >>> list(d.keys())
        ['a', 'b', 'z']
        """
        try:
            self.__keys.remove(key)
        except ValueError:
            raise KeyError(key)
        return super().__delitem__(key)


    def __setitem__(self, key, value):
        """If key is in the dictionary, sets its value to value;
        otherwise adds the key to the dictionary with the given value
        >>> d = SortedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d["t"] = -17
        >>> d["z"] = 43
        >>> d["@"] = -11
        >>> x = d["m"] = 22
        >>> x == 22
        True
        >>> d["r"] = 5
        >>> list(d.keys())
        ['@', 'a', 'i', 'm', 'n', 'r', 's', 't', 'y', 'z']
        """
        if key not in self:
            self.__keys.add(key)
        return super().__setitem__(key, value)


    def __repr__(self):
        return object.__repr__(self)


    def __str__(self):
        return ("{" + ", ".join(["{0!r}: {1!r}".format(k, v)
                                 for k, v in self.items()]) + "}")


    def copy(self):
        """Returns a shallow copy of the dictionary with the same
        key function
        >>> d = SortedDict(dict(V=1, E=2, I=3, N=4, S=5))
        >>> e = d.copy()
        >>> str(e)
        "{'E': 2, 'I': 3, 'N': 4, 'S': 5, 'V': 1}"
        >>> import copy
        >>> f = copy.copy(d)
        >>> str(f)
        "{'E': 2, 'I': 3, 'N': 4, 'S': 5, 'V': 1}"
        """
        d = SortedDict()
        super(SortedDict, d).update(self)
        d.__keys = self.__keys.copy()
        return d

    __copy__ = copy



if __name__ == "__main__":
    import doctest
    doctest.testmod()
-----------------------------------------------------------------------------------------------------------------------------------------------------

SortedList.py
>>> L = SortedList((5, 8, -1, 3, 4, 22))
>>> L[2] = 18 #doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
...
TypeError: use add() to insert a value and rely on the...
>>> list(L)
[-1, 3, 4, 5, 8, 22]
>>> L.add(5)
>>> L.add(5)
>>> L.add(6)
>>> list(L)
[-1, 3, 4, 5, 5, 5, 6, 8, 22]
>>> L.index(4)
2
>>> L.count(5), L.count(2)
(3, 0)
>>> L.insert(2, 9)
Traceback (most recent call last):
...
AttributeError: 'SortedList' object has no attribute 'insert'
>>> L.reverse()
Traceback (most recent call last):
...
AttributeError: 'SortedList' object has no attribute 'reverse'
>>> L.sort()
Traceback (most recent call last):
...
AttributeError: 'SortedList' object has no attribute 'sort'
>>> import collections
>>> isinstance(L, collections.Sequence)
False
"""

_identity = lambda x: x


class SortedList:

    def __init__(self, sequence=None, key=None):
        """Creates a SortedList that orders using < on the items,
        or on the results of using the given key function
        >>> L = SortedList()
        >>> print(L)
        []
        >>> L = SortedList((5, 8, -1, 3, 4, 22))
        >>> print(L)
        [-1, 3, 4, 5, 8, 22]
        >>> L = SortedList({9, 8, 7, 6, -1, -2})
        >>> print(L)
        [-2, -1, 6, 7, 8, 9]
        >>> L = SortedList([-5, 4, -3, 8, -2, 16, -1, 0, -3, 8])
        >>> print(L)
        [-5, -3, -3, -2, -1, 0, 4, 8, 8, 16]
        >>> L2 = SortedList(L)
        >>> print(L2)
        [-5, -3, -3, -2, -1, 0, 4, 8, 8, 16]
        >>> L = SortedList(("the", "quick", "brown", "fox", "jumped"))
        >>> print(L)
        ['brown', 'fox', 'jumped', 'quick', 'the']
        """
        self.__key = key or _identity
        assert hasattr(self.__key, "__call__")
        if sequence is None:
            self.__list = []
        elif (isinstance(sequence, SortedList) and
              sequence.key == self.__key):
            self.__list = sequence.__list[:]
        else:
            self.__list = sorted(list(sequence), key=self.__key)


    @property
    def key(self):
        """Return the key function used by this list
        """
        return self.__key


    def clear(self):
        """Clears the list
        >>> L = SortedList((5, 8, -1, 3, 4, 22))
        >>> print(L)
        [-1, 3, 4, 5, 8, 22]
        >>> L.clear()
        >>> print(L)
        []
        """
        self.__list = []


    def __bisect_left(self, value):
        """Returns value's key and its index position in the list
        (or where value belongs if it isn't in the list)
        """
        key = self.__key(value)
        left, right = 0, len(self.__list)
        while left < right:
            middle = (left + right) // 2
            if self.__key(self.__list[middle]) < key:
                left = middle + 1
            else:
                right = middle
        return key, left


    def add(self, value):
        """Adds a value to the list (duplicates are allowed)
        >>> L = SortedList((5, 8, -1, 3, 4, 22))
        >>> print(L)
        [-1, 3, 4, 5, 8, 22]
        >>> L.add(5)
        >>> L.add(5)
        >>> L.add(7)
        >>> L.add(-18)
        >>> L.add(99)
        >>> print(L)
        [-18, -1, 3, 4, 5, 5, 5, 7, 8, 22, 99]
        """
        index = self.__bisect_left(value)[1]
        if index == len(self.__list):
            self.__list.append(value)
        else:
            self.__list.insert(index, value)


    def pop(self, index=-1):
        """Removes and returns the item the given index
        >>> L = SortedList([-18, -1, 3, 4, 5, 5, 7, 8, 22, 99])
        >>> print(L)
        [-18, -1, 3, 4, 5, 5, 7, 8, 22, 99]
        >>> L.pop()
        99
        >>> L.pop(0)
        -18
        >>> L.pop(5)
        7
        >>> print(L)
        [-1, 3, 4, 5, 5, 8, 22]
        >>> L.pop(12)
        Traceback (most recent call last):
        ...
        IndexError: pop index out of range
        """
        return self.__list.pop(index)


    def remove(self, value):
        """Removes the first occurrence of value from the list
        >>> L = SortedList([-18, -1, 3, 4, 5, 5, 7, 8, 22, 99])
        >>> print(L)
        [-18, -1, 3, 4, 5, 5, 7, 8, 22, 99]
        >>> L.remove(20)
        Traceback (most recent call last):
        ...
        ValueError: SortedList.remove(x): x not in list
        >>> L.remove(5)
        >>> L.remove(-18)
        >>> L.remove(99)
        >>> print(L)
        [-1, 3, 4, 5, 7, 8, 22]
        >>> L = SortedList(["ABC", "X", "abc", "Abc"], lambda x: x.lower())
        >>> print(L)
        ['ABC', 'abc', 'Abc', 'X']
        >>> L.remove("Abca")
        Traceback (most recent call last):
        ...
        ValueError: SortedList.remove(x): x not in list
        >>> print(L)
        ['ABC', 'abc', 'Abc', 'X']
        >>> L.remove("Abc")
        >>> print(L)
        ['ABC', 'abc', 'X']
        >>> L.remove("ABC")
        >>> print(L)
        ['abc', 'X']
        >>> L.remove("X")
        >>> print(L)
        ['abc']
        >>> L.remove("abc")
        >>> print(L)
        []
        """
        key, index = self.__bisect_left(value)
        while (index < len(self.__list) and
                self.__key(self.__list[index]) == key):
            if self.__list[index] == value:
                del self.__list[index]
                return
            index += 1
        raise ValueError("{0}.remove(x): x not in list".format(
                            self.__class__.__name__))


    def remove_every(self, value):
        """Removes every occurrence of value from the list
        Returns the number of occurrences removed (which could be 0).
        >>> L = SortedList([5, 5, -18, -1, 3, 4, 5, 5, 7, 8, 22, 99])
        >>> L.add(5)
        >>> L.add(5)
        >>> print(L)
        [-18, -1, 3, 4, 5, 5, 5, 5, 5, 5, 7, 8, 22, 99]
        >>> L.remove_every(-3)
        0
        >>> L.remove_every(7)
        1
        >>> L.remove_every(5)
        6
        >>> print(L)
        [-18, -1, 3, 4, 8, 22, 99]
        >>> L = SortedList(["ABC", "X", "abc", "Abc"], lambda x: x.lower())
        >>> L.remove_every("abc")
        3
        """
        count = 0
        key, index = self.__bisect_left(value)
        while (index < len(self.__list) and
               self.__key(self.__list[index]) == key):
            del self.__list[index]
            count += 1
        return count


    def count(self, value):
        """Counts every occurrence of value in the list
        >>> L = SortedList([5, 5, -18, -1, 3, 4, 5, 5, 7, 8, 22, 99])
        >>> L.count(5)
        4
        >>> L.count(99)
        1
        >>> L.count(-17)
        0
        >>> L = SortedList(["ABC", "X", "abc", "Abc"], lambda x: x.lower())
        >>> L.count("abc")
        3
        """
        count = 0
        key, index = self.__bisect_left(value)
        while (index < len(self.__list) and
               self.__key(self.__list[index]) == key):
            index += 1
            count += 1
        return count


    def index(self, value):
        """Returns the index position of the first occurrence of value
        >>> L = SortedList([5, 5, -18, -1, 3, 4, 7, 8, 22, 99, 2, 1, 3])
        >>> L.index(5)
        7
        >>> L.index(0)
        Traceback (most recent call last):
        ...
        ValueError: SortedList.index(x): x not in list
        >>> L.index(99)
        12
        >>> L = SortedList(["ABC", "X", "abc", "Abc"], lambda x: x.lower())
        >>> print(L)
        ['ABC', 'abc', 'Abc', 'X']
        >>> L.index("x")
        3
        >>> L.index("abc")
        0
        """
        key, index = self.__bisect_left(value)
        if (index < len(self.__list) and
            self.__key(self.__list[index]) == key):
            return index
        raise ValueError("{0}.index(x): x not in list".format(
                         self.__class__.__name__))


    def __delitem__(self, index):
        """Deletes the value at the given index position
        >>> L = SortedList([9, -5, 3, -7, 8, 14, 0, 8, 3])
        >>> print(L)
        [-7, -5, 0, 3, 3, 8, 8, 9, 14]
        >>> del L[0]
        >>> del L[-1]
        >>> del L[5]
        >>> print(L)
        [-5, 0, 3, 3, 8, 9]
        >>> del L[25]
        Traceback (most recent call last):
        ...
        IndexError: list assignment index out of range
        >>> del L[-3:]
        >>> print(L)
        [-5, 0, 3]
        """
        del self.__list[index]
        

    def __getitem__(self, index):
        """Returns the value at the given index position
        >>> L = SortedList([9, -5, 3, -7, 8, 14, 0, 8, 3])
        >>> L[0], L[3], L[4], L[-1]
        (-7, 3, 3, 14)
        >>> L[15]
        Traceback (most recent call last):
        ...
        IndexError: list index out of range
        >>> L[:3]
        [-7, -5, 0]
        >>> L[4:8]
        [3, 8, 8, 9]
        """
        return self.__list[index]


    def __setitem__(self, index, value):
        raise TypeError("use add() to insert a value and rely on "
                        "the list to put it in the right place")


    def __iter__(self):
        """Returns an iterator for the list
        >>> L = SortedList([5, 5, -18, -1, 3, 4, 7, 8, 22, 99, 2, 1, 3])
        >>> result = []
        >>> for x in L:
        ...     result.append(x)
        >>> print(result)
        [-18, -1, 1, 2, 3, 3, 4, 5, 5, 7, 8, 22, 99]
        """
        return iter(self.__list)


    def __reversed__(self):
        """Returns a reverse iterator for the list
        >>> L = SortedList([5, 5, -18, -1, 3, 4, 7, 8, 22, 99, 2, 1, 3])
        >>> result = []
        >>> for x in reversed(L):
        ...     result.append(x)
        >>> print(result)
        [99, 22, 8, 7, 5, 5, 4, 3, 3, 2, 1, -1, -18]
        """
        return reversed(self.__list)


    def __contains__(self, value):
        """Returns True if value is in the list; otherwise returns False
        >>> L = SortedList([5, 5, -18, -1, 3, 4, 7, 8, 22, 99, 2, 1, 3])
        >>> 5 in L
        True
        >>> 0 in L
        False
        >>> 99 in L
        True
        >>> L = SortedList(["ABC", "X", "Abc"], lambda x: x.lower())
        >>> "abc" in L
        True
        >>> "x" in L
        True
        >>> "ZZ" in L
        False
        """
        key, index = self.__bisect_left(value)
        return (index < len(self.__list) and
                self.__key(self.__list[index]) == key)


    def __len__(self):
        """Returns the length of the list
        >>> L = SortedList([5, 5, -18, -1, 3, 4, 7, 8, 22, 99, 2, 1, 3])
        >>> len(L)
        13
        >>> L = SortedList()
        >>> len(L)
        0
        """
        return len(self.__list)


    def __str__(self):
        """Returns a human readable string version of the list; the
        result could be very long
        >>> L = SortedList([-1, 3, 4, 7, 8, 22, -9, 2, 1, 3])
        >>> str(L)
        '[-9, -1, 1, 2, 3, 3, 4, 7, 8, 22]'
        >>> L = SortedList()
        >>> str(L)
        '[]'
        >>> L = SortedList(("the", "quick", "brown", "fox", "jumped"))
        >>> str(L)
        "['brown', 'fox', 'jumped', 'quick', 'the']"
        """
        return str(self.__list)


    def copy(self):
        """Returns a shallow copy of the list with the same key function
        >>> L = SortedList([-1, 3, 4, 7, 8, 22, -9, 2, 1, 3])
        >>> m = L.copy()
        >>> str(m)
        '[-9, -1, 1, 2, 3, 3, 4, 7, 8, 22]'
        >>> m[:]
        [-9, -1, 1, 2, 3, 3, 4, 7, 8, 22]
        >>> import copy
        >>> n = copy.copy(L)
        >>> str(n)
        '[-9, -1, 1, 2, 3, 3, 4, 7, 8, 22]'
        """
        return SortedList(self, self.__key)
        
    __copy__ = copy

if __name__ == "__main__":
    import doctest
    doctest.testmod()