
import re


def validation(file):

    file1 = open(file, 'r')
    count = 0
    valid = True

    while True:
        line = file1.readline()
        line = line.replace('\n', '')
        if not line:
            break
        count += 1
        if count % 4 == 2:
            if re.findall('([^A|T|C|G|N])', line).__len__() > 0:
                valid = False
                break

    if count % 4 != 0:
        valid = False

    return valid
