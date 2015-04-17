#!/usr/bin/python
import sys
import re
import string

variables = {}
outs = {}
monomial = "([a-zA-z]+\d+)"
mn = re.compile(monomial)

def extractValues(strin):
        xAddr1 = strin[2].strip()
        xAddr2 = strin[4].strip()
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
            x2 = bool(int(xAddr2))
        return {'x1':x1, 'x2':x2}

if len(sys.argv) != 3:
    raise Exception("Usage: equationReader <input file> <output file>")

fin = open(sys.argv[1], "r")


lines = fin.readlines()
inputs = re.compile("\d+ inputs")
outputs = re.compile("\d+ outputs")
for index, line in enumerate(lines):
    if inputs.match(line):
        #Creation of the x set
        xLine = lines[index + 1]
        xValueLine = lines[index + 2]
        ins = string.split(xLine)
        insValues = string.split(xValueLine)
        if len(ins) != len(insValues):
            print(line + xLine + xValueLine)
            raise Exception("equationReader: you need to provide a starting value for each x inserted")
        for i in range(len(ins)):
            x = ins[i].strip()
            variables[x] = bool(int(insValues[i]))
    else:
        if outputs.match(line):
            #Creation of the y set
            yLine = lines[index + 1]
            ins = string.split(yLine, " ")
            for y in ins:
                y.strip()
                outs[y] = None
            else:
                if line == "begin":
                    #When the equations start we get to the next cicle which performs the calculations
                    break

#y = x + z
equation_XOR = re.compile(monomial + " = " + monomial + " \+ (" + monomial + "|(0|1))")
#y = x * z
equation_AND = re.compile(monomial + " = " + monomial + " \* (" + monomial + "|(0|1))")
#y = x
equation_ASSIGNEMENT = re.compile(monomial + " = (" + monomial + "|(0|1))")

for index, line in enumerate(lines):
    tmp = string.split(line, " ")
    print(line)
    if equation_XOR.match(line):
        xdict = extractValues(tmp)
        yAddr = tmp[0]
        y = xdict['x1'] ^ xdict['x2']
        variables[yAddr] = y
        if yAddr in outs:
            outs[yAddr] = y
    else:
        if equation_AND.match(line):
            xdict = extractValues(tmp)
            yAddr = tmp[0]
            y = xdict['x1'] & xdict['x2']
            variables[yAddr] = y
            if yAddr in outs:
                outs[yAddr] = y
        else:
            if equation_ASSIGNEMENT.match(line):
                yAddr = tmp[0].strip()
                xAddr = tmp[2].strip()
                if mn.match(xAddr):
                    if xAddr in variables:
                        x = variables[xAddr]
                    else:
                        raise Exception("equationReader: variable " + xAddr + " not found")
                else:
                    x = bool(xAddr)
                y = x
                variables[yAddr] = y
                if yAddr in outs:
                    outs[yAddr] = y
            else:
                print("Skipping malformed equation:" + line)

#Printing out the results
fin.close()
fout = open(sys.argv[2], "w")
for key, value in outs.items():
    fout.write(key + " = {}\n".format(int(value)))
fout.close()
