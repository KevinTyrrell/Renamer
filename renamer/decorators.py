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

        :return: None
        """
        self.__decorated.operate()
        shift = self.__shift
        files = self.get_files()
        v: int  # Treat raw object values as int-type.
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

        :return: None
        """
        self.__decorated.operate()
        files = self.get_files()

        it = enumerate(files.keys())
        model = next(it)[1]  # Select one file to use as the 'model' for the directory
        regexp = "([0-9]+)"

        # Map of indexes which start runs of integers --> the value of those integers.
        model_ixs = {m.start(): int(model[m.start():m.end()]) for m in finditer(regexp, model)}
        target_ixs = {}

        for e in it:  # Find numerical differences between the model and this file.
            ixs = {m.start(): int(e[1][m.start():m.end()]) for m in finditer(regexp, e[1])}
            for k, v in ixs.items():
                # Determine what integers the two file names do not have in common
                if k in model_ixs and model_ixs[k] != v:
                    target_ixs[k] = v
            break  # No need to check the entire file list

        if len(target_ixs) > 1:
            raise Exception("NumeratedDecorator: A numerated pattern could not be differentiated: ", target_ixs)
        if len(target_ixs) <= 0:
            raise Exception("NumeratedDecorator: A numerated pattern does not exist in the directory")
        target_ixs = next(enumerate(target_ixs.keys()))[1]
        regexp = compile(regexp)

        def parse_file_name(filename: str):
            match = regexp.match(filename, target_ixs)
            if not match:
                raise Exception("NumeratedDecorator: A numerated pattern does not exist in the directory")
            return int(match.group(0))
        for k in files.keys():
            files[k] = parse_file_name(k)
