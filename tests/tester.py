import unittest

from directory import Directory


class MyTestCase(unittest.TestCase):
    def test_directory(self):
        d = Directory("C:\\Users\\admin\\Desktop\\Test\\test")
        print(d)
        print(d.get_files)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
