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

import unittest

import sys
from io import StringIO
from core.renamer import main


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.prog_stdout = StringIO()
        sys.stdout = self.prog_stdout
        self.test_args = [ "renamer.py" ]

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_version(self):
        sys.argv = self.test_args + ["-v"]
        main()
        self.prog_stdout.seek(0)
        result = self.prog_stdout.read().strip()
        print(result)


if __name__ == '__main__':
    unittest.main()
