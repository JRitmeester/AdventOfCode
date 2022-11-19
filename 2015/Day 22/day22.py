import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))
from util.project import load_input_data
input_ = load_input_data(day=22, year=2015)


def first():
    return None


def second():
    return None


print(first())
print(second())
