import unittest

import pandas

from Codes.Preprocessing import validation, merging_sequence_files


class MyTestCase(unittest.TestCase):
    def test_sequence_valid(self):
        path = "../../resource/subsra/ERR209506.fastq"
        res = validation(path)
        self.assertEqual(True, res)  # add assertion here

    def test_sequence_invalid(self):
        path = "../../resource/subsra/SRR2545599.fastq"
        res = validation(path)
        self.assertEqual(False, res)  # add assertion here

    def test_merging_sequence_files(self):
        in_dir = "../../resource/subsra/"
        out_dir = in_dir + "merge.fasta"
        lables = ['Isolated', 'Amplicon', 'Amplicon', 'Isolated', 'Metagenome', 'Metagenome', 'SAGs', 'Metagenome',
                  'Amplicon', 'Amplicon', 'Metagenome', 'Amplicon', 'Metagenome', 'Metagenome', 'SAGs', 'Metagenome', 'Isolated',
                  'Metagenome', 'Amplicon', 'Isolated', 'Isolated', 'Metagenome', 'SAGs', 'Amplicon', 'SAGs',
                  'Metagenome', 'Amplicon', 'Amplicon', 'Isolated', 'Metagenome', 'Isolated', 'Metagenome', 'SAGs',
                  'Isolated', 'SAGs', 'SAGs', 'Isolated', 'Amplicon', 'Amplicon', 'Isolated', 'Isolated']
        merging_sequence_files(in_dir, out_dir, lables)
        data = pandas.read_csv(out_dir, header=None)
        nr = data.shape[0]
        nc = data.shape[1]
        self.assertEqual(nr, 40) # The SRR2545599.fastq is not valid
        self.assertEqual(nc, 3)


if __name__ == '__main__':
    unittest.main()
