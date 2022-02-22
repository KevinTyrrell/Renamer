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

from typing import Dict
from re import finditer, compile
from math import log, ceil

from directory import Directory, FileMetadata
from util.util import require_non_none


class ExtensionDecorator(Directory):
    def __init__(self, decorated: Directory, ext: str):
        """
        Decorator which modifies the file extension of all files in the directory

        :param decorated: Decorated directory
        :param ext: Extension to be set
        """
        self.__decorated = require_non_none(decorated)
        self.__ext = require_non_none(ext)

    def get_files(self) -> Dict[str, FileMetadata]:
        return self.__decorated.get_files()

    def operate(self) -> None:
        self.__decorated.operate()
        files, ext = self.get_files(), self.__ext
        for k, v in files.items():
            v.ext = ext


class FormatDecorator(Directory):
    def __init__(self, decorated: Directory, fmt: str):
        """
        Decorator which modifies the output filename into a specified format

        The format string must contain a '$d' specifier, designated for the numerical pattern.
        e.g. [4.doc, 5.doc] -> FormatDecorator("Homework ($d)") -> [Homework (4).doc, Homework (5).doc]

        :param decorated: Decorated directory
        :param fmt: Format to be applied to the output file
        """
        self.__decorated = require_non_none(decorated)
        self.__fmt = require_non_none(fmt)

    def get_files(self) -> Dict[str, FileMetadata]:
        return self.__decorated.get_files()

    def operate(self) -> None:
        self.__decorated.operate()
        files, fmt = self.get_files(), self.__fmt
        for k, v in files.items():
            v.fmt = fmt


class ZeroesDecorator(Directory):
    def __init__(self, decorated: Directory, digits: int = 0):
        """
        Decorator which inserts leading zeroes preceding the numerical value

        e.g. [7.png, 300.png] -> ZeroesDecorator(3) -> [007.png, 300.png]

        :param decorated: Decorated directory
        :param digits: Number of desired digits for the numerical value (0 for automatic)
        """
        self.__decorated = require_non_none(decorated)
        self.__digits = require_non_none(digits)

    def get_files(self) -> Dict[str, FileMetadata]:
        return self.__decorated.get_files()

    def operate(self) -> None:
        self.__decorated.operate()
        files = self.get_files()
        large = max(map(lambda x: x.num, files.values()))
        digits = max(self.__digits, self.__count_digits(large))
        for k, v in files.items():
            v.fnum = (digits - self.__count_digits(v.num)) * "0" + str(v.num)

    @staticmethod
    def __count_digits(num: int):
        """
        :param num: Number to count digits of
        :return: Number of digits present
        """
        return int(ceil(log(num + 1, 10)))


class ShifterDecorator(Directory):
    def __init__(self, decorated: Directory, shift: int):
        """
        Decorator which shifts all numerical values in filenames by a specified offset

        e.g. [50.mkv] -> ShifterDecorator(-5) -> [45.mkv]

        :param decorated: Decorated directory
        :param shift: int Offset to shift by
        """
        self.__decorated = require_non_none(decorated)
        self.__shift = require_non_none(shift)
        if shift == 0:
            raise ValueError("File number shift is invalid: " + shift)

    def get_files(self) -> Dict[str, FileMetadata]:
        return self.__decorated.get_files()

    def operate(self) -> None:
        self.__decorated.operate()
        files, shift = self.get_files(), self.__shift
        for k, v in files.items():
            v.num = v.num + shift


class FlattenDecorator(Directory):
    def __init__(self, decorated: Directory):
        """
        Decorator which flattens the numerical pattern, ensuring all files are consecutive

        e.g. [ "15.avi", "24.avi", "101.avi" ] -> [ "15.avi", "16.avi", "17.avi" ]

        :param decorated: Decorated directory
        """
        self.__decorated = require_non_none(decorated)

    def get_files(self) -> Dict[str, FileMetadata]:
        return self.__decorated.get_files()

    def operate(self) -> None:
        self.__decorated.operate()
        files = self.get_files()
        if len(files) <= 1:
            return  # A directory of zero or one files is already flattened

        sort = sorted(files.items(), key=lambda t: t[1].num)
        first: FileMetadata = sort[0][1]
        small = int(first.num)  # Redundant cast
        for i in range(1, len(files)):  # Skip first (smallest) element
            v: FileMetadata = sort[i][1]
            v.num = small + i


class NumeratedDecorator(Directory):
    def __init__(self, decorated: Directory):
        """
        Decorator which initializes the numerical pattern according to the filenames in the directory.
        This decorator is an initialization operation and must be called before other decorators.

        e.g. [ "MyPhoto34HighRes.png", "MyPhoto36HighRes.png" ] ->
                { "MyPhoto34HighRes.png": 34, "MyPhoto36HighRes.png": 36 }

        :param decorated: Decorated directory
        """
        self.__decorated = require_non_none(decorated)

    def get_files(self) -> Dict[str, FileMetadata]:
        return self.__decorated.get_files()

    def operate(self) -> None:
        self.__decorated.operate()
        files = self.get_files()

        it = enumerate(files.keys())
        model = next(it)[1]  # Select one file to use as the 'model' for the directory
        regexp = "([0-9]+)"

        # Map of indexes which start runs of integers --> the value of those integers
        model_ixs = {m.start(): int(model[m.start():m.end()]) for m in finditer(regexp, model)}
        target_ixs = {}

        for e in it:  # Find numerical differences between the model and this file
            ixs = {m.start(): int(e[1][m.start():m.end()]) for m in finditer(regexp, e[1])}
            for k, v in ixs.items():
                # Determine what integers the two file names do not have in common
                if k in model_ixs and model_ixs[k] != v:
                    target_ixs[k] = v
            break  # No need to check the entire file list

        if len(target_ixs) > 1:
            raise Exception("A numerated pattern could not be differentiated: ", target_ixs)
        if len(target_ixs) <= 0:
            raise Exception("A numerated pattern is not present in the directory")
        target_ixs = next(enumerate(target_ixs.keys()))[1]
        regexp = compile(regexp)
        unique_keys = set()  # Ensure that keys are 1:1

        def parse_file_name(filename: str) -> int:
            match = regexp.match(filename, target_ixs)
            if not match:
                raise Exception("File does not contain a numerical index: " + filename)
            match = int(match.group(0))
            if match in unique_keys:
                raise Exception("File numerical values are not one-to-one: " + filename)
            unique_keys.add(match)
            return match
        for k, v in files.items():
            v.num = parse_file_name(k)
