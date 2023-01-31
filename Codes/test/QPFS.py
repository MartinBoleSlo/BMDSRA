import unittest

import numpy as np
import pandas
import pandas as pd

from Codes.QPFS import QPFS


class MyTestCase(unittest.TestCase):

    def test_weight(self):
        path = "..\\..\\resource\\3-features\\small-features.csv"
        data = pandas.read_csv(path)
        data.drop(columns='id', inplace=True)
        nc = data.shape[1] - 1
        qp = QPFS(data)
        importance_matrix = qp.get_weight()
        print(importance_matrix)
        most_important = importance_matrix.iloc[0, 0]
        self.assertEqual(most_important, "ent_tsal_38")  # add assertion here

    def test_uncertainty_matrix(self):
        path = "..\\..\\resource\\3-features\\small-features.csv"
        data = pandas.read_csv(path)
        data.drop(columns='id', inplace=True)
        nc = data.shape[1] - 1
        qp = QPFS(data)
        qp.symmetric_uncertainty()
        print(qp.uncertainty_matrix)
        second_element = qp.uncertainty_matrix[0, 1]
        self.assertAlmostEqual(second_element, 0.81489743, places=5)  # add assertion here

    def test_discretize(self):
        path = "..\\..\\resource\\3-features\\small-features.csv"
        data = pandas.read_csv(path)
        data.drop(columns='id', inplace=True)
        nc = data.shape[1] - 1
        qp = QPFS(data, 'label')
        qp.discretize(bins=10)
        first_element = qp.data.iloc[0, 0]
        print(qp.data)
        self.assertEqual(first_element, 9)  # add assertion here

    def test_QP(self):
        path = "..\\..\\resource\\3-features\\H.csv"
        data = pd.read_csv(path, header=None).to_numpy()
        nc = data.shape[0]
        nf = nc - 1
        H = data[0:nf, 0:nf]
        f = data[0:nf, nf]
        q = QPFS()
        weights = q.solve_QP(H, f, 0)
        ord = np.argsort(weights)[::-1]
        print(ord)
        self.assertEqual(ord[0], 10)
        self.assertEqual(ord[1], 9)
        self.assertEqual(ord[2], 11)


if __name__ == '__main__':
    unittest.main()
