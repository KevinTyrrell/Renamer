import unittest

from directory import ConcreteDirectory
from decorators import ShifterDecorator, NumeratedDecorator, FlattenDecorator, ZeroesDecorator


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
        sort = sorted(files.values())
        for i in range(len(files)):
            self.assertEqual(sort[i] - sort[0], i)

    def test_zeroes_decorator1(self):
        d = ConcreteDirectory("C:\\Users\\admin\\Desktop\\Test\\test")
        d = NumeratedDecorator(d)
        d = ZeroesDecorator(d, 3)
        d.operate()
        files = d.get_files()
        sort = sorted(files.values())
        self.assertEqual(sort[0], "007")


if __name__ == '__main__':
    unittest.main()
