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
from typing import List

from util.util import require_non_none


class Directory(ABC):
    @abstractmethod
    def get_files(self) -> List[str]:
        """
        :return: List of files in the directory.
        """
        pass

    @abstractmethod
    def operate(self) -> None:
        """
        Performs an operation on the directory.
        :return: None
        """
        pass


class DirDecorator(Directory, ABC):
    def __init__(self, directory: Directory):
        """
         Decorates a directory, adding additional functionality.
        :param directory: Directory to be decorated.
        """
        self.__decorated = require_non_none(directory)

    def operate(self) -> None:
        # Recursively call the decorated operation.
        self.__decorated.operate()
