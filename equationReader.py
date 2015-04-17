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
            variables[ins[i]] = bool(insValues[i])
    else if line.find("outputs", beg=0, end=len(line)):
        #Creation of the y set
        yLine = next(fin)
        ins = string.split(xLine, " ")
        for y in ins:
            outs [y] = None
    else if line.find("begin", beg = 0, end = len(line)):
        #When the equations start we get to the next cicle which performs the calculations
        break

monomial = "([a-zA-z]+\d+)"
mn = re.compile(monomial)
#y = x + z
equation_XOR = re.compile(monomial + " = " + monomial + " \+ " + monomial + "|(0|1)")
#y = x * z
equation_AND = re.compile(monomial + " = " + monomial + " \* " + monomial + "|(0|1)")
#y = x
equation_ASSIGNEMENT = re.compile(monomial + " = " + monomial + "|(0|1)")

for line in fin:
    if !(line.find("end", beg = 0, end = len(line))):
        tmp = string.split(line, " ")
        if equation_XOR.match(line):
            yAddr = tmp[0]
            xAddr1 = tmp[2]
            xAddr2 = tmp[4]
            if xAddr1 in variables:
                x1 = variables[xAddr1]
            else:
                raise Exception("equationReader: variable " + xAddr1 + " not found")
            if mn.match(xAddr2):
                if xAddr2 in variables:
                    x2 = variables[xAddr2]
                else:
                    raise Exception("equationReader: variable " + xAddr2 + " not found")
            else:
                x2 = int(xAddr2)
            variables[yAddr] =
    else:
        break
