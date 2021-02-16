import sys

from fail_pass import passed
from urls import URL
import os

BASE_DIR = "/home/ubuntu/contest/w_test"
# BASE_DIR = ""
PREREQUISITE_FILE = "prerequisite"


def main_func(url, port, test_number, prerequisite_path=BASE_DIR):
    
    if prerequisite_path != None:
        fp = open(os.path.join(prerequisite_path, PREREQUISITE_FILE))
    else:
        fp = open(PREREQUISITE_FILE)
    test_array = []
    for i, line in enumerate(fp):
        if i == test_number - 1:
            test_array = str(line).split()

    fp.close()

    for i in test_array:
        module = __import__(i)
        func = getattr(module, i)
        url_class = URL()
        url_class.base_url = url + ":" + str(port)
        return_value = func(url_class)
        if return_value != passed(i) or i == test_array[len(test_array) - 1]:
            return return_value


if __name__ == "__main__":
    a, b = sys.argv
    url, port, test_number = str(b).split(',')
    print(main_func(url, port, int(test_number), None))

