import unittest

from Codes.Sudolf import Sudolf


class MyTestCase(unittest.TestCase):
    def test_sudolf(self):
        temp_dir = "c:\\temp"
        out_dir = "resource\\subsra"
        num_spots = 10
        length_spots = 10
        num_thread = 5
        sdf = Sudolf(temp_dir, out_dir, num_spots, length_spots, num_thread)
        sdf.get("SRR3927025", 37358802)


if __name__ == '__main__':
    unittest.main()
