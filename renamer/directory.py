"""
    CLI tool written in Python 3 used to systemically rename files in a directory while adhering to a variety of criteria.
    Copyright (C) 2022  Kevin Tyrrell

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from abc import abstractmethod, ABC
from typing import Dict
from os import listdir, rename
from os.path import isdir, join
from re import compile

from util.util import require_non_none


class FileMetadata:
    # Pattern to extract extensions from filenames
    __ext_pattern = compile(r"^.*\.([^.]+)$")
    __fmt_specifier = "$d"

    def __init__(self, filename: str):
        """
        Constructs metadata for a specified file.

        The following metadata is tracked:
        * name: Original filename with extension
        * fmt: Output format of the file, which must contain '$d' (file number)
        * num: File number (unknown during initialization)
        * fnum: Formatted number, used to override 'num'
        * ext: Extension of the file

        :param filename: Name of the file
        """
        self.__name = require_non_none(filename)
        self.__fmt = FileMetadata.__fmt_specifier
        self.__num = None
        self.__fnum = None
        match = FileMetadata.__ext_pattern.match(filename)
        if match is None:
            raise ValueError("The following file must contain an extension: " + filename)
        self.__ext = match.group(1)
    
    @property
    def name(self) -> str:
        return self.__name

    @property
    def fmt(self) -> str:
        return self.__fmt

    @fmt.setter
    def fmt(self, fmt: str) -> None:
        if FileMetadata.__fmt_specifier not in require_non_none(fmt):
            raise ValueError("Required format specified '{}' was not found in the following format: {}"
                             .format(FileMetadata.__fmt_specifier, fmt))
        self.__fmt = fmt

    @property
    def num(self) -> int:
        return self.__num

    @num.setter
    def num(self, num: int) -> None:
        self.__num = require_non_none(num)

    @property
    def fnum(self) -> str:
        if self.__num is None:
            raise Exception("File's number cannot be formatted as it was uninitialized: " + self.__name)
        if self.__fnum is None:
            self.__fnum = str(self.__num)
        return self.__fnum

    @fnum.setter
    def fnum(self, fnum: str) -> None:
        self.__fnum = require_non_none(fnum)

    @property
    def ext(self) -> str:
        return self.__ext

    @ext.setter
    def ext(self, ext: str) -> None:
        self.__ext = require_non_none(ext)

    def __str__(self) -> str:
        """
        Formats the filename according to the object's metadata.

        :return: Formatted filename of the object
        """
        return self.fmt.replace("$d", self.fnum) + "." + self.ext


class Directory(ABC):
    @abstractmethod
    def get_files(self) -> Dict[str, FileMetadata]:
        """
        :rtype: object
        :return: Relation of filenames to their numerical ordering.
        """
        pass

    @abstractmethod
    def operate(self) -> None:
        """
        Performs an operation on the directory.

        :return: None
        """
        pass


class ConcreteDirectory(Directory):
    def __init__(self, path: str):
        self.__path = require_non_none(path)
        if not isdir(path):
            raise Exception("Path is not a valid directory: {}".format(path))
        self.__files = {e: FileMetadata(e) for e in listdir(path)}

    def save_files(self) -> None:
        """
        Saves the directory to the storage medium.

        File name changes made to the directory object are renamed.

        :return: None
        """

        """
        Determine the correct order to rename files such that no rename conflicts arise.
        1st Pass: Classify operations as either conflict-free or waiting on another operation.
        2nd Pass: Pop safe operations -> update status of operations that were waiting on them.
        """
        operations = {k: str(v) for (k, v) in self.__files.items()}
        performable = []  # Rename operations which can be performed without conflicts.
        conflicts = {}  # Rename operations that wait on another rename operation.

        for k, v in operations.items():
            if v not in operations:
                performable.append(k)
            else:
                conflicts[v] = k
        while len(performable) > 0:
            op = performable.pop()
            p1 = join(self.__path, op)
            p2 = join(self.__path, operations[op])
            rename(p1, p2)
            if op in conflicts:
                performable.append(conflicts[op])
                del conflicts[op]

    def get_files(self) -> Dict[str, FileMetadata]:
        return self.__files

    def operate(self) -> None:
        pass  # Sentinel method.
