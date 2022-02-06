import unittest

import renamer


class MyTestCase(unittest.TestCase):
    def test_directory(self):
        renamer.Directory()
        d = directory()
        print("Done")
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
