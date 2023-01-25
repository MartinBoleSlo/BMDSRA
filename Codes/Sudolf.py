import os
import random
import shutil
import subprocess
import tempfile
from random import randint

from tqdm import tqdm


class Sudolf:
    """
    : param tempdir: the address of a temporary directory for storing
    : param out: the address of the output directory which the downloaded file should be stored
    : param ns: the number of spots
    : param ls: the length of spots
    : param nt: the number of threads
    : param to: the time out of downloading based on minutes
    : param seed: a number for seed for random subsampling
    : param silent:
    """
    total_spots = 0
    accession_number = ""
    path_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path_fastq_dump = os.path.join(path_base, "stoolkit")

    def __init__(self, tempdir, out, ns, ls, nt, to=20, seed=7, silent=True):
        self.num_spots = ns
        self.length_spots = ls
        self.out_dir = os.path.join(self.path_base, out)
        self.threads = nt
        self.temp_base = tempdir
        self.tmp_dir = tempfile.TemporaryDirectory(prefix="Sudolf_", dir=self.temp_base)
        self.timeOut = to * 60
        self.seed = seed
        self.silent = silent

    def __del__(self):
        self.tmp_dir.cleanup()

    """
    : param accession: The accession number of the sequence file
    : param total_spot: The number of total spot of the sequence file.   
    """

    def get(self, accession, total_spot):
        self.accession_number = accession
        self.total_spots = total_spot

        if not self.parameters_validation():
            return -1

        random.seed(self.seed)
        random_points = set()
        while len(random_points) < self.num_spots:
            random_points.add(randint(0, total_spot))
        random_points = list(random_points)
        random_points.sort()
        queue_points = []
        [queue_points.append(i) for i in random_points]

        batch_size = self.threads
        pbar = tqdm(total=self.num_spots, leave=False, position=1, ncols=80, desc=self.accession_number)

        try:
            while len(queue_points) > 0:
                n = min(batch_size, len(queue_points))
                ps = []
                starts = []
                for j in range(0, n):
                    start = queue_points.pop()
                    starts.append(start)
                    ps.append(self.run_dump(self.accession_number, start))

                for j in range(0, len(ps)):
                    try:
                        exit_code = ps[j].wait(timeout=self.timeOut)
                        if exit_code != 0:
                            queue_points.append(starts[j])
                        else:
                            pbar.update(1)
                    except subprocess.TimeoutExpired:
                        queue_points.append(starts[j])
                        ps[j].terminate()

            wfd = {}
            for point in random_points:
                tmp_path = os.path.join(self.tmp_dir.name, str(point))
                for fo in os.listdir(tmp_path):
                    if fo not in wfd:
                        wfd[fo] = open(os.path.join(self.out_dir, fo), "wb")
                    with open(os.path.join(tmp_path, fo), "rb") as fd:
                        shutil.copyfileobj(fd, wfd[fo])

        except Exception as e:
            print(e)
        finally:
            pbar.close()
            path = self.tmp_dir.name
            if os.path.isdir(path):
                shutil.rmtree(path)

    def parameters_validation(self):
        msg = ""
        if self.total_spots < 5 * self.num_spots:
            msg = "The length of sequence is so low, total spot of {0} is {1} ".format(self.accession_number,
                                                                                       self.total_spots)
        elif not os.path.isdir(self.tmp_dir.name):
            msg = "The temporary directory does not exist: {0}".format(self.tmp_dir.name)
        if msg != "":
            print(msg)
            return False
        else:
            return True

    def run_dump(self, acc, start):
        path = os.path.join(self.tmp_dir.name, str(start))
        if os.path.isdir(path):
            shutil.rmtree(path)
        os.mkdir(path)
        end_point = start + self.length_spots - 1
        cmd = ["cd", self.path_fastq_dump, "&", "fastq-dump", "-X", str(start), "-N", str(end_point), "-O", path, acc]
        if self.silent:
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            p = subprocess.Popen(cmd, shell=True)
        return p
