import pandas as pd
import re
import itertools as IT
import tempfile
import os


def unique(pth, sep=''):
    def name_sequence():
        count = IT.count()
        yield ''
        while True:
            yield '{s}{n:d}'.format(s = sep, n = next(count))
    orig = tempfile._name_sequence
    with tempfile._once_lock:
        tempfile._name_sequence = name_sequence()
        pth = os.path.normpath(pth)
        dirname, basename = os.path.split(pth)
        filename, ext = os.path.splitext(basename)
        fd, filename = tempfile.mkstemp(dir=dirname, prefix = filename, suffix = ext)
        tempfile._name_sequence = orig
    return filename


def condition(obj, words):
    if any(i in obj.lower() for i in words):
        return True
    else:
        return False


m_rem = pd.read_csv("assets/m_rem.csv")
path = "output/apple_employees_linkedin_profiles.xlsx"
df = pd.read_excel(path)
target = df["title"]

# for i in target.tolist():
#     print(i)


words = ["opera", "recrui", "cap", "analy", "data"]
words_set1 = words = ["opera", "recrui"]
bool_val = target.apply(lambda x: condition(x, words))
df = df[bool_val]
print(df.shape)
df.to_excel(unique(path), index=False)