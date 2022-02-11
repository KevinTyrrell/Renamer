import unittest

from directory import ConcreteDirectory
from decorators import ShifterDecorator, NumeratedDecorator


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


if __name__ == '__main__':
    unittest.main()
