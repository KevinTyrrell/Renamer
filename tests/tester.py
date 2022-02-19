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
import re

from directory import ConcreteDirectory
from decorators import ShifterDecorator, NumeratedDecorator, FlattenDecorator, ZeroesDecorator, FormatDecorator, ExtensionDecorator


class MyTestCase(unittest.TestCase):
    def test_directory(self):
        d = ConcreteDirectory("C:\\Users\\admin\\Desktop\\Test\\test")
        self.assertEqual(True, True)

    def test_shift_decorator1(self):
        d = ConcreteDirectory("C:\\Users\\admin\\Desktop\\Test\\test")
        d.operate()
        d = ShifterDecorator(d, 5)
        with self.assertRaises(Exception):
            d.operate()

    def test_shift_decorator2(self):
        d = ConcreteDirectory("C:\\Users\\admin\\Desktop\\Test\\test")
        d = NumeratedDecorator(d)
        d = ShifterDecorator(d, 5)
        d.operate()
        files = d.get_files()
        for k, v in files.items():
            self.assertEqual(type(v).__class__, int.__class__)

    def test_nume_decorator1(self):
        d = ConcreteDirectory("C:\\Users\\admin\\Desktop\\Test\\test")
        d = NumeratedDecorator(d)
        d.operate()

    def test_flatten_decorator1(self):
        d = ConcreteDirectory("C:\\Users\\admin\\Desktop\\Test\\test")
        d = NumeratedDecorator(d)
        d = FlattenDecorator(d)
        d.operate()
        files = d.get_files()
        sort = sorted(files.values(), key=lambda x: x.num)
        for i in range(len(files)):
            self.assertEqual(sort[i].num - sort[0].num, i)

    def test_zeroes_decorator1(self):
        d = ConcreteDirectory("C:\\Users\\admin\\Desktop\\Test\\test")
        d = NumeratedDecorator(d)
        d = ZeroesDecorator(d, 3)
        d.operate()
        files = d.get_files()
        sort = sorted(files.values(), key=lambda x: x.num)
        self.assertEqual(len(sort[0].fnum), 3)

    def test_format_decorator1(self):
        d = ConcreteDirectory("C:\\Users\\admin\\Desktop\\Test\\test")
        d = NumeratedDecorator(d)
        d = FormatDecorator(d, "%s")
        self.assertRaises(ValueError, lambda: d.operate())

    def test_format_decorator2(self):
        d = ConcreteDirectory("C:\\Users\\admin\\Desktop\\Test\\test")
        d = NumeratedDecorator(d)
        d = FormatDecorator(d, "My Test Episode ($d)")
        d.operate()
        files = d.get_files()
        f = next(enumerate(files.values()))
        f: str = str(f[1])
        self.assertTrue(re.match(r"My Test Episode \([0-9]+\)", f))

    def test_ext_decorator1(self):
        d = ConcreteDirectory("C:\\Users\\admin\\Desktop\\Test\\test")
        d = NumeratedDecorator(d)
        d = ExtensionDecorator(d, "jpeg")
        d.operate()
        for e in d.get_files().values():
            self.assertTrue(str(e).endswith(".jpeg"))

    def test_directory_save1(self):
        a = ConcreteDirectory("C:\\Users\\admin\\Desktop\\Test\\test")
        d = NumeratedDecorator(a)
        d = ShifterDecorator(d, 1)
        d.operate()
        a.save_files()


if __name__ == '__main__':
    unittest.main()
