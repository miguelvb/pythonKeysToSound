#!/usr/bin/python

import os
import string
printable = set(string.printable)

def to_ascii(s):
 return filter(lambda x: x in printable, s)

dir_ = "./sounds/wav/"

for (dirpath, dirnames, filenames) in os.walk(dir_):
    for filename in filenames:
        if filename.endswith(".wav"):
            filepath = dirpath + '/' + filename
            print filepath
            file_ = to_ascii(filepath)
            print file_
            os.rename(filepath, file_)