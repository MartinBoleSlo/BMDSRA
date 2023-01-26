import unittest

import pandas

from Codes.QPFS import QPFS


class MyTestCase(unittest.TestCase):

    def test_something(self):
        path = "..\\..\\resource\\rawdata\\small.csv"
        data = pandas.read_csv(path)
        data.drop(columns='id', inplace=True)
        nc = data.shape[1] - 1
        qp = QPFS(data, nc)
        qp.symmetric_uncertainty()
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
