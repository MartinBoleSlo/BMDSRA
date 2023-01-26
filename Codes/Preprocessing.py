import glob
import os.path
import re
import pandas as pd
import tqdm
import re


def validation(file):
    valid = True
    with open(file) as file:
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
