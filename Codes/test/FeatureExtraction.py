import unittest

import pandas

from Codes.FeatureExtraction import FeatureExtraction


class MyTestCase(unittest.TestCase):

    path = "..\\..\\resource\\subsra\\merge.fasta"
    data = pandas.read_csv(path, header=None, names=['id', 'seq', 'label'])
    seq = data.iloc[0, 1]
    obj_fe = FeatureExtraction(seq)
    def test_entropy_shannon(self):
        windows = [1, 5]
        res_shannon = self.obj_fe.entropy_based(windows, method="shannon")
        print(res_shannon)
        self.assertAlmostEqual(res_shannon[0], 1.993666262325747, places=5)
        self.assertAlmostEqual(res_shannon[1], 9.878718681634492, places=5)

    def test_entropy_tsallis(self):
        windows = [1, 5]
        res_tsallis = self.obj_fe.entropy_based(windows, method="Tsallis")
        print(res_tsallis)
        self.assertAlmostEqual(res_tsallis[0], 0.7472380340506508, places=5)
        self.assertAlmostEqual(res_tsallis[1], 0.998817761373957, places=5)

    def test_fourier(self):
        res_furier = self.obj_fe.fourier_based(method="zcurve")
        print(res_furier)
        self.assertAlmostEqual(res_furier[16], 724.6194251, places=5)
        self.assertAlmostEqual(res_furier[17], 0.004140098, places=5)
        self.assertAlmostEqual(res_furier[18], 0.070961083, places=5)

if __name__ == '__main__':
    unittest.main()
