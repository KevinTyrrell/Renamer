import unittest

from directory import ConcreteDirectory
from decorators import ShifterDecorator


class MyTestCase(unittest.TestCase):
    def test_directory(self):
        d = ConcreteDirectory("C:\\Users\\admin\\Desktop\\Test\\test")
        print(d)
        print(d.get_files)
        self.assertEqual(True, True)

    def test_shift_decorator(self):
        d = ConcreteDirectory("C:\\Users\\admin\\Desktop\\Test\\test")
        d.operate()
        d = ShifterDecorator(d, 5)
        with self.assertRaises(Exception):
            d.operate()


if __name__ == '__main__':
    unittest.main()
