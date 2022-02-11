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

from directory import Directory
from util.util import require_non_none


class ShifterDecorator(Directory):
    def __init__(self, decorated: Directory, shift: int):
        self.__decorated = require_non_none(decorated)
        self.__shift = require_non_none(shift)
        if shift == 0:
            raise ValueError("File shift of 0 is invalid")

    def get_files(self) -> Dict[str, object]:
        return self.__decorated.get_files()

    def operate(self) -> None:
        """
        Shifts the numerical value of each file in the directory by a specified amount.
        :return:
        """
        shift = self.__shift
        files = self.get_files()
        v: int  # Values are initialized to 'None' but are in practicality integers.
        for k, v in files.items():
            if v is None:
                raise Exception("ShiftDecorator cannot be applied until file numbers have been initialized")
            files[k] = v + shift


class NumeratedDecorator(Directory):
    def __init__(self, decorated: Directory):
        self.__decorated = require_non_none(decorated)

    def get_files(self) -> Dict[str, object]:
        return self.__decorated.get_files()

    def operate(self) -> None:
        """
        Associates all files in a directory with a unique numerical value.
        :return:
        """
        files = self.get_files()
        v: int  # Values are initialized to 'None' but are in practicality integers.
        for k, v in files.items():
            pass
