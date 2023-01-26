import unittest

import pandas

from Codes.FeatureExtraction import FeatureExtraction


class MyTestCase(unittest.TestCase):
    def test_entropy(self):
        path = "..\\..\\resource\\subsra\\merge.fasta"
        data = pandas.read_csv(path, header=None, names=['id', 'seq', 'label'])
        seq = data.iloc[0, 1]
        windows = [1, 5]
        fe = FeatureExtraction(seq)
        res_shannon = fe.entropy_based(windows, method="shannon")
        res_tsallis = fe.entropy_based(windows, method="Tsallis")
        print(res_shannon)
        print(res_tsallis)
        self.assertAlmostEqual(res_shannon[0], 1.993666262325747, places=5)
        self.assertAlmostEqual(res_shannon[1], 9.878718681634492, places=5)
        self.assertAlmostEqual(res_tsallis[0], 0.7472380340506508, places=5)
        self.assertAlmostEqual(res_tsallis[1], 0.998817761373957, places=5)



if __name__ == '__main__':
    unittest.main()
