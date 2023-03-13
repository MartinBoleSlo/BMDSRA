import os
import unittest

from Codes.BMDSRA import BMDSRA


class MyTestCase(unittest.TestCase):

    model_path = "..\\..\\resource\\4-model\\model.json"
    scaler_path = "..\\..\\resource\\4-model\\scaler.gz"
    model = BMDSRA(model_path, scaler_path)
    def test_model_Isolated(self):
        seq_path = "..\\..\\resource\\2-subsra\\SRR1588386.fastq"
        res = self.model.predict(seq_path)
        self.assertEqual(res, "Isolated")  # add assertion here

    def test_model_Amplicon(self):
        #
        seq_path = "..\\..\\resource\\2-subsra\\SRR5923239.fastq"
        res = self.model.predict(seq_path)
        self.assertEqual(res, "Amplicon")

        seq_path = "..\\..\\resource\\2-subsra\\SRR1196387.fastq"
        res = self.model.predict(seq_path)
        self.assertEqual(res, "Amplicon")

    def test_model_Metagenome(self):

        seq_path = "..\\..\\resource\\2-subsra\\SRR5215510.fastq"
        res = self.model.predict(seq_path)
        self.assertEqual(res, "Metagenome")

        seq_path = "..\\..\\resource\\2-subsra\\DRR171797.fastq"
        res = self.model.predict(seq_path)
        self.assertEqual(res, "Metagenome")

    def test_model_directorz(self):
        # read files in folder
        # iterate through all file
        seq_path = "C:/My Research/08- BioSeC/06-BethaTest/"
        os.chdir(seq_path)
        for file in os.listdir():
            # Check whether file is in text format or not
            if file.endswith(".fastq"):
                file_path = f"{seq_path}/{file}"
                res = self.model.predict(file_path)
                print(res)

if __name__ == '__main__':
    unittest.main()
