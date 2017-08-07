BikeStock.py
import struct
import BinaryRecordFile


class Bike:

    def __init__(self, identity, name, quantity, price):
        assert len(identity) > 3, ("invalid bike identity '{0}'"
                                   .format(identity))
        self.__identity = identity
        self.name = name
        self.quantity = quantity
        self.price = price


    @property
    def identity(self):
        "The bike's identity"
        return self.__identity


    @property
    def name(self):
        "The bike's name"
        return self.__name

    @name.setter
    def name(self, name):
        assert len(name), "bike name must not be empty"
        self.__name = name


    @property
    def quantity(self):
        "How many of this bike are in stock"
        return self.__quantity

    @quantity.setter
    def quantity(self, quantity):
        assert 0 <= quantity, "quantity must not be negative"
        self.__quantity = quantity


    @property
    def price(self):
        "The bike's price"
        return self.__price

    @price.setter
    def price(self, price):
        assert 0.0 <= price, "price must not be negative"
        self.__price = price


    @property
    def value(self):
        "The value of these bikes in stock"
        return self.quantity * self.price


_BIKE_STRUCT = struct.Struct("<8s30sid")


def _bike_from_record(record):
    ID, NAME, QUANTITY, PRICE = range(4)
    parts = list(_BIKE_STRUCT.unpack(record))
    parts[ID] = parts[ID].decode("utf8").rstrip("\x00")
    parts[NAME] = parts[NAME].decode("utf8").rstrip("\x00")
    return Bike(*parts)


def _record_from_bike(bike):
    return _BIKE_STRUCT.pack(bike.identity.encode("utf8"),
                             bike.name.encode("utf8"),
                             bike.quantity, bike.price)


class BikeStock:

    def __init__(self, filename):
        self.__file = BinaryRecordFile.BinaryRecordFile(filename,
                                                _BIKE_STRUCT.size)
        self.__index_from_identity = {}
        for index in range(len(self.__file)):
            record = self.__file[index]
            if record is not None:
                bike = _bike_from_record(record)
                self.__index_from_identity[bike.identity] = index


    def close(self):
        "Compacts and closes the file"
        self.__file.inplace_compact()
        self.__file.close()


    def append(self, bike):
        "Adds a new bike to the stock"
        index = len(self.__file)
        self.__file[index] = _record_from_bike(bike)
        self.__index_from_identity[bike.identity] = index
        

    def __delitem__(self, identity):
        "Deletes the stock record for the specified bike"
        del self.__file[self.__index_from_identity[identity]]
        del self.__index_from_identity[identity]


    def __getitem__(self, identity):
        "Retrieves the stock record for the specified bike"
        record = self.__file[self.__index_from_identity[identity]]
        return None if record is None else _bike_from_record(record)


    def __change_bike(self, identity, what, value):
        index = self.__index_from_identity[identity]
        record = self.__file[index]
        if record is None:
            return False
        bike = _bike_from_record(record)
        if what == "price" and value is not None and value >= 0.0:
            bike.price = value
        elif what == "name" and value is not None:
            bike.name = value
        else:
            return False
        self.__file[index] = _record_from_bike(bike)
        return True

    change_name = lambda self, identity, name: self.__change_bike(
                                            identity, "name", name)
    change_name.__doc__ = "Changes the bike's name"

    change_price = lambda self, identity, price: self.__change_bike(
                                            identity, "price", name)
    change_price.__doc__ = "Changes the bike's price"


    def __change_stock(self, identity, amount):
        index = self.__index_from_identity[identity]
        record = self.__file[index]
        if record is None:
            return False
        bike = _bike_from_record(record)
        bike.quantity += amount
        self.__file[index] = _record_from_bike(bike)
        return True
        
    increase_stock = (lambda self, identity, amount:
                                self.__change_stock(identity, amount))
    increase_stock.__doc__ = ("Increases the stock held for the "
                              "specified bike by by the given amount")

    decrease_stock = (lambda self, identity, amount:
                                self.__change_stock(identity, -amount))
    decrease_stock.__doc__ = ("Decreases the stock held for the "
                              "specified bike by by the given amount")

        
    def __iter__(self):
        for index in range(len(self.__file)):
            record = self.__file[index]
            if record is not None:
                yield _bike_from_record(record)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
---------------------------------------------------------------------------------------------------------------------------------------------------
BikeStock_ans.py


import struct
import BinaryRecordFile_ans as BinaryRecordFile


class Bike:

    def __init__(self, identity, name, quantity, price):
        assert len(identity) > 3, ("invalid bike identity '{0}'"
                                   .format(identity))
        self.__identity = identity
        self.name = name
        self.quantity = quantity
        self.price = price


    @property
    def identity(self):
        "The bike's identity"
        return self.__identity


    @property
    def name(self):
        "The bike's name"
        return self.__name

    @name.setter
    def name(self, name):
        assert len(name), "bike name must not be empty"
        self.__name = name


    @property
    def quantity(self):
        "How many of this bike are in stock"
        return self.__quantity

    @quantity.setter
    def quantity(self, quantity):
        assert 0 <= quantity, "quantity must not be negative"
        self.__quantity = quantity


    @property
    def price(self):
        "The bike's price"
        return self.__price

    @price.setter
    def price(self, price):
        assert 0.0 <= price, "price must not be negative"
        self.__price = price


    @property
    def value(self):
        "The value of these bikes in stock"
        return self.quantity * self.price


_BIKE_STRUCT = struct.Struct("<8s30sid")


def _bike_from_record(record):
    ID, NAME, QUANTITY, PRICE = range(4)
    parts = list(_BIKE_STRUCT.unpack(record))
    parts[ID] = parts[ID].decode("utf8").rstrip("\x00")
    parts[NAME] = parts[NAME].decode("utf8").rstrip("\x00")
    return Bike(*parts)


def _record_from_bike(bike):
    return _BIKE_STRUCT.pack(bike.identity.encode("utf8"),
                             bike.name.encode("utf8"),
                             bike.quantity, bike.price)


class BikeStock:

    def __init__(self, filename):
        self.__file = BinaryRecordFile.BinaryRecordFile(filename,
                                                _BIKE_STRUCT.size)
        self.__index_from_identity = {}
        for index in range(len(self.__file)):
            record = self.__file[index]
            if record is not None:
                bike = _bike_from_record(record)
                self.__index_from_identity[bike.identity] = index


    def close(self):
        "Closes the file"
        self.__file.close()


    def append(self, bike):
        "Adds a new bike to the stock"
        index = len(self.__file)
        self.__file.append(_record_from_bike(bike))
        self.__index_from_identity[bike.identity] = index
        

    def __delitem__(self, identity):
        "Deletes the stock record for the specified bike"
        index = self.__index_from_identity[identity]
        del self.__file[index]
        del self.__index_from_identity[identity]
        for key, value in self.__index_from_identity.items():
            if value > index:
                self.__index_from_identity[key] = value - 1


    def __getitem__(self, identity):
        "Retrieves the stock record for the specified bike"
        record = self.__file[self.__index_from_identity[identity]]
        return None if record is None else _bike_from_record(record)


    def __change_bike(self, identity, what, value):
        index = self.__index_from_identity[identity]
        record = self.__file[index]
        if record is None:
            return False
        bike = _bike_from_record(record)
        if what == "price" and value is not None and value >= 0.0:
            bike.price = value
        elif what == "name" and value is not None:
            bike.name = value
        else:
            return False
        self.__file[index] = _record_from_bike(bike)
        return True

    change_name = lambda self, identity, name: self.__change_bike(
                                            identity, "name", name)
    change_name.__doc__ = "Changes the bike's name"

    change_price = lambda self, identity, price: self.__change_bike(
                                            identity, "price", name)
    change_price.__doc__ = "Changes the bike's price"


    def __change_stock(self, identity, amount):
        index = self.__index_from_identity[identity]
        record = self.__file[index]
        if record is None:
            return False
        bike = _bike_from_record(record)
        bike.quantity += amount
        self.__file[index] = _record_from_bike(bike)
        return True
        
    increase_stock = (lambda self, identity, amount:
                                self.__change_stock(identity, amount))
    increase_stock.__doc__ = ("Increases the stock held for the "
                              "specified bike by by the given amount")

    decrease_stock = (lambda self, identity, amount:
                                self.__change_stock(identity, -amount))
    decrease_stock.__doc__ = ("Decreases the stock held for the "
                              "specified bike by by the given amount")

        
    def __iter__(self):
        for index in range(len(self.__file)):
            record = self.__file[index]
            if record is not None:
                yield _bike_from_record(record)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
---------------------------------------------------------------------------------------------------------------------------------------------------

BinaryRecordFile.py

import os
import struct
import tempfile


_DELETED = b"\x01"
_OKAY = b"\x02"


class BinaryRecordFile:

    def __init__(self, filename, record_size, auto_flush=True):
        """A random access binary file that behaves rather like a list
        with each item a bytes or bytesarray object of record_size.
        """
        self.__record_size = record_size + 1
        mode = "w+b" if not os.path.exists(filename) else "r+b"
        self.__fh = open(filename, mode)
        self.auto_flush = auto_flush


    @property
    def record_size(self):
        "The size of each item"
        return self.__record_size - 1


    @property
    def name(self):
        "The name of the file"
        return self.__fh.name


    def flush(self):
        """Flush writes to disk
        Done automatically if auto_flush is True
        """
        self.__fh.flush()


    def close(self):
        self.__fh.close()


    def __setitem__(self, index, record):
        """Sets the item at position index to be the given record
        The index position can be beyond the current end of the file.
        """
        assert isinstance(record, (bytes, bytearray)), \
               "binary data required"
        assert len(record) == self.record_size, (
            "record must be exactly {0} bytes".format(
            self.record_size))
        self.__fh.seek(index * self.__record_size)
        self.__fh.write(_OKAY)
        self.__fh.write(record)
        if self.auto_flush:
            self.__fh.flush()


    def __getitem__(self, index):
        """Returns the item at the given index position
        If there is no item at the given position, raises an
        IndexError exception.
        If the item at the given position has been deleted returns
        None.
        """
        self.__seek_to_index(index)
        state = self.__fh.read(1)
        if state != _OKAY:
            return None
        return self.__fh.read(self.record_size)
        

    def __seek_to_index(self, index):
        if self.auto_flush:
            self.__fh.flush()
        self.__fh.seek(0, os.SEEK_END)
        end = self.__fh.tell()
        offset = index * self.__record_size
        if offset >= end:
            raise IndexError("no record at index position {0}".format(
                             index))
        self.__fh.seek(offset)


    def __delitem__(self, index):
        """Deletes the item at the given index position.
        See undelete()
        """
        self.__seek_to_index(index)
        state = self.__fh.read(1)
        if state != _OKAY:
            return
        self.__fh.seek(index * self.__record_size)
        self.__fh.write(_DELETED)
        if self.auto_flush:
            self.__fh.flush()


    def undelete(self, index):
        """Undeletes the item at the given index position.
        If an item is deleted it can be undeleted---providing compact()
        (or inplace_compact()) has not been called.
        """
        self.__seek_to_index(index)
        state = self.__fh.read(1)
        if state == _DELETED:
            self.__fh.seek(index * self.__record_size)
            self.__fh.write(_OKAY)
            if self.auto_flush:
                self.__fh.flush()
            return True
        return False


    def __len__(self):
        """The number number of record positions.
        This is the maximum number of records there could be at
        present. The true number may be less because some records
        might be deleted. After calling compact() (or
        inplace_compact()), this returns the true number.
        """
        if self.auto_flush:
            self.__fh.flush()
        self.__fh.seek(0, os.SEEK_END)
        end = self.__fh.tell()
        return end // self.__record_size


    def compact(self, keep_backup=False):
        """Eliminates blank and deleted records"""
        compactfile = self.__fh.name + ".$$$"
        backupfile = self.__fh.name + ".bak"
        self.__fh.flush()
        self.__fh.seek(0)
        fh = open(compactfile, "wb")
        while True:
            data = self.__fh.read(self.__record_size)
            if not data:
                break
            if data[:1] == _OKAY:
                fh.write(data)
        fh.close()
        self.__fh.close()

        os.rename(self.__fh.name, backupfile)
        os.rename(compactfile, self.__fh.name)
        if not keep_backup:
            os.remove(backupfile)
        self.__fh = open(self.__fh.name, "r+b")


    def inplace_compact(self):
        """Eliminates blank and deleted records in-place preserving the
        original order
        """
        index = 0
        length = len(self)
        while index < length:
            self.__seek_to_index(index)
            state = self.__fh.read(1)
            if state != _OKAY:
                for next in range(index + 1, length):
                    self.__seek_to_index(next)
                    state = self.__fh.read(1)
                    if state == _OKAY:
                        self[index] = self[next]
                        del self[next]
                        break
                else:
                    break
            index += 1
        self.__seek_to_index(0)
        state = self.__fh.read(1)
        if state != _OKAY:
            self.__fh.truncate(0)
        else:
            limit = None
            for index in range(len(self) - 1, 0, -1):
                self.__seek_to_index(index)
                state = self.__fh.read(1)
                if state != _OKAY:
                    limit = index
                else:
                    break
            if limit is not None:
                self.__fh.truncate(limit * self.__record_size)
        self.__fh.flush()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
---------------------------------------------------------------------------------------------------------------------------------------------------

BinaryRecordFile_ans.py

import os
import struct
import tempfile


class BinaryRecordFile:

    def __init__(self, filename, record_size, auto_flush=True):
        """A random access binary file that behaves rather like a list
        with each item a bytes or bytesarray object of record_size.
        """
        self.__record_size = record_size
        mode = "w+b" if not os.path.exists(filename) else "r+b"
        self.__fh = open(filename, mode)
        self.auto_flush = auto_flush


    @property
    def record_size(self):
        "The size of each item"
        return self.__record_size


    @property
    def name(self):
        "The name of the file"
        return self.__fh.name


    def flush(self):
        """Flush writes to disk
        Done automatically if auto_flush is True
        """
        self.__fh.flush()


    def close(self):
        self.__fh.close()


    def append(self, record):
        """Adds a new record"""
        assert isinstance(record, (bytes, bytearray)), \
               "binary data required"
        assert len(record) == self.record_size, (
            "record must be exactly {0} bytes".format(
            self.record_size))
        self.__fh.seek(0, os.SEEK_END)
        self.__fh.write(record)
        if self.auto_flush:
            self.__fh.flush()


    def __setitem__(self, index, record):
        """Sets the item at position index to be the given record
        The index position can be beyond the current end of the file.
        """
        assert isinstance(record, (bytes, bytearray)), \
               "binary data required"
        assert len(record) == self.record_size, (
            "record must be exactly {0} bytes".format(
            self.record_size))
        self.__seek_to_index(index)
        self.__fh.write(record)
        if self.auto_flush:
            self.__fh.flush()


    def __getitem__(self, index):
        """Returns the item at the given index position
        If there is no item at the given position, raises an
        IndexError exception.
        If the item at the given position has been deleted returns
        None.
        """
        self.__seek_to_index(index)
        return self.__fh.read(self.record_size)
        

    def __seek_to_index(self, index):
        if self.auto_flush:
            self.__fh.flush()
        self.__fh.seek(0, os.SEEK_END)
        end = self.__fh.tell()
        offset = index * self.record_size
        if offset >= end:
            raise IndexError("no record at index position {0}".format(
                             index))
        self.__fh.seek(offset)


    def __delitem__(self, index):
        """Deletes the item at the given index position and moves the
        following records up.
        """
        length = len(self)
        for following in range(index + 1, length):
            self[index] = self[following]
            index += 1
        self.__fh.truncate((length - 1) * self.record_size)
        self.__fh.flush()


    def __len__(self):
        """The number number of records."""
        if self.auto_flush:
            self.__fh.flush()
        self.__fh.seek(0, os.SEEK_END)
        end = self.__fh.tell()
        return end // self.record_size


if __name__ == "__main__":
    import doctest
    doctest.testmod()
---------------------------------------------------------------------------------------------------------------------------------------------------
xdump.py

import optparse
import os
import sys


def main():
    parser = optparse.OptionParser(
                usage="usage: %prog [options] file1 [file2 [... fileN]]")
    parser.add_option("-b", "--blocksize", dest="blocksize", type="int",
            help="block size (8..80) [default: %default]")
    parser.add_option("-d", "--decimal", dest="decimal",
            action="store_true",
            help="decimal block numbers [default: hexadecimal]")
    parser.add_option("-e", "--encoding", dest="encoding",
            help="encoding (ASCII..UTF-32) [default: %default]")
    parser.set_defaults(blocksize=16, decimal=False, encoding="UTF-8")
    opts, files = parser.parse_args()
    if not (8 <= opts.blocksize <= 80):
        parser.error("invalid blocksize")
    if not files:
        parser.error("no files specified")

    for i, filename in enumerate(files):
        if i:
            print()
        if len(files) > 1:
            print("File:", filename)
        xdump(filename, opts.blocksize, opts.encoding, opts.decimal)


def xdump(filename, blocksize, encoding, decimal):
    encoding_text = "{0} characters".format(encoding.upper())
    width = (blocksize * 2) + (blocksize // 4)
    if blocksize % 4:
        width += 1
    print("Block     Bytes{0:{1}} {2}".format("", (width - 5),
                                              encoding_text))
    print("--------  {0}  {1}".format("-" * (width - 1),
          "-" * max(len(encoding_text), blocksize)))
    block_number_format = "{0:08} " if decimal else "{0:08X} "
    block_number = 0
    fh = None
    try:
        fh = open(filename, "rb")
        while True:
            data = fh.read(blocksize)
            if not data:
                break
            line = [block_number_format.format(block_number)]
            chars = []
            for i, b in enumerate(data):
                if i % 4 == 0:
                    line.append(" ")
                line.append("{0:02X}".format(b))
                chars.append(b if 32 <= b < 127 else ord("."))
            for i in range(len(data), blocksize):
                if i % 4 == 0:
                    line.append(" ")
                line.append("  ")
            line.append("  ")
            line.append(bytes(chars).decode(encoding, "replace")
                        .replace("\uFFFD", "."))
            print("".join(line))
            block_number += 1
    except EnvironmentError as err:
        print(err)
    finally:
        if fh is not None:
            fh.close()


main()
