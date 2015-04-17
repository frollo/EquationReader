#!/usr/bin/python
import sys
import re

if len(sys.argv) != 3:
    raise Exception("Usage: equationReader <input file> <output file>")
fin = open(sys.argv[1], "r")
fout = open(sys.argv[2], "w")

for line in fin:
    if line.find("inputs" , beg=0, end=len(line)):
        inputLine = next(fin)
