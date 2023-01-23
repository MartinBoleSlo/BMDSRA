import unittest

from Codes.Preprocessing import validation


class MyTestCase(unittest.TestCase):
    def test_sequence_valid(self):
        path = "../../resource/subsra/ERR209506.fastq"
        res = validation(path)
        self.assertEqual(True, res)  # add assertion here

    def test_sequence_invalid(self):
        path = "../../resource/subsra/SRR2545599.fastq"
        res = validation(path)
        self.assertEqual(False, res)  # add assertion here


if __name__ == '__main__':
    unittest.main()
