import unittest

from Codes.BMDSRA import BMDSRA


class MyTestCase(unittest.TestCase):
    def test_model(self):
        model_path = "..\\..\\resource\\4-model\\model.json"
        seq_path = "..\\..\\resource\\2-subsra\\SRR1588386.fastq"
        model = BMDSRA(model_path)
        res = model.predict(seq_path)
        self.assertEqual(res, "Isolated")  # add assertion here


if __name__ == '__main__':
    unittest.main()
