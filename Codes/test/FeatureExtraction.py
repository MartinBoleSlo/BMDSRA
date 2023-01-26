import unittest

import pandas


class MyTestCase(unittest.TestCase):
    def test_entropy_shannon(self):
        path = ""
        pandas.read_csv(path)
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
