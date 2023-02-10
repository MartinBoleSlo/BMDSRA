import glob
import os.path
import re
import pandas as pd
import tqdm
import re
import random
from random import randint


def validation(path):
    valid = True
    with open(path) as file:
        for num, line in enumerate(file, start=1):
            line = line.replace('\n', '')
            if not line:
                break
            if num % 4 == 2:
                if re.findall('([^A|T|C|G|N])', line).__len__() > 0:
                    valid = False
                    break

    return valid


def merging_sequence_files(in_directory, out_directory, labels):
    paths = glob.glob(in_directory + "*.fastq")
    outfile = open(out_directory, 'w')
    count = 0
    for filename in tqdm.tqdm(paths):
        count += 1
        if validation(filename):
            with open(filename) as file:
                lines = file.readlines()
                identity = re.findall(r"@\w+", lines[0])[0]
                identity = identity.replace("@", "") + ","
                outfile.write(identity)
                record = ""
                for i in range(1, len(lines), 4):
                    record += lines[i].strip()
                record += "," + labels[count % len(labels)]
                record += "\n"
                outfile.write(record)
        else:
            print("The sequence file {0}-{1} is not valid".format(count, os.path.basename(filename)))
    outfile.close()
    df = pd.read_csv(out_directory, sep=",", header=None)
    df = df.sample(frac=1).reset_index(drop=True)
    df.to_csv(out_directory, index=False, header=None)


def sampling(path, ns=300, ls=10, seed=7):
    random.seed(seed)
    random_points = set()
    num_lines = 0
    with open(path, 'r') as fp:
        num_lines = sum(1 for line in fp)
    num_lines = int(num_lines / 4)

    if num_lines < ns * ls:
        message = "The file is shorter than threshold ({0} < {1}).".format(num_lines, ns)
        raise Exception(message)
    elif num_lines < ns * ls * ls:
        random_points = range(1, ns * ls, ls)
    else:
        while len(random_points) < ns:
            random_points.add(randint(0, num_lines))

    random_points = list(random_points)
    random_points.sort()

    random_indexes = []
    for point in random_points:
        win = range(point, point+ls, 1)
        random_indexes.append(list(win))
    random_indexes = sum(random_indexes, [])

    seq = []
    with open(path) as file:
        for num, line in enumerate(file, start=1):
            num = (num - 2) / 4 + 1
            if num == int(num) and int(num) in random_indexes:
                seq.append(line.replace('\n', ''))
    return ''.join(seq)
