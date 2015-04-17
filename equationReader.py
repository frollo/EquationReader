#!/usr/bin/python
import sys
import re

if len(sys.argv) != 3:
    raise Exception("Usage: equationReader <input file> <output file>")

fin = open(sys.argv[1], "r")

variables = {}
outs = {}
for line in fin:
    if line.find("inputs" , beg=0, end=len(line)):
        #Creation of the x set
        xLine = next(fin)
        xValueLine = next(fin)
        ins = string.split(xLine, " ")
        insValues = string.split(xValueLine, " ")
        if len(ins) != len(insValues):
            raise Exception("equationReader: you need to provide a starting value for each x inserted")
        for i in range(len(ins)):
            tmp = int(insValues[i])
            if (tmp != 0) & (tmp != 1):
                raise Exception("equationReader: you need to provide binary values")
            variables[ins[i]] = tmp
    else if line.find("outputs", beg=0, end=len(line)):
        #Creation of the y set
        yLine = next(fin)
        ins = string.split(xLine, " ")
        for y in ins:
            outs [y] = None
    else if line.find("begin", beg = 0, end = len(line)):
        #When the equations start we get to the next cicle which performs the calculations
        break
