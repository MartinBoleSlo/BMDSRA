import glob
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


def merging_sequence_files(in_directory, out_directory):
    paths = glob.glob(in_directory + "*.fastq")
    outfile = open(out_directory, 'w')
    for filename in tqdm.tqdm(paths):
        with open(filename) as file:
            lines = file.readlines()
            identity = re.findall(r"@\w+", lines[0])[0]
            identity = identity.replace("@", "") + ","
            outfile.write(identity)
            record = ""
            for i in range(1, len(lines), 4):
                record += lines[i].strip()
            record += "\n"
            outfile.write(record)
    outfile.close()
    df = pd.read_csv(out_directory, sep=",", header=None)
    df = df.sample(frac=1).reset_index(drop=True)
    df.to_csv(out_directory, index=False, header=None)
