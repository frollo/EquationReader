#!/usr/bin/python
import sys
import re
import string

variables = {}
outs = {}
monomial = "([a-zA-z]+\d+)"
mn = re.compile(monomial)

a = 0
def extractValues(strin):
        xAddr1 = strin[2]
        xAddr2 = strin[4]
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
            x2 = bool(xAddr2)
        return {'x1':x1, 'x2':x2}

if len(sys.argv) != 3:
    raise Exception("Usage: equationReader <input file> <output file>")

fin = open(sys.argv[1], "r")


for line in fin:
    b=len(line)
    if line.find("inputs" , a, b):
        #Creation of the x set
        xLine = next(fin)
        xValueLine = next(fin)
        ins = string.split(xLine, " ")
        insValues = string.split(xValueLine, " ")
        if len(ins) != len(insValues):
            raise Exception("equationReader: you need to provide a starting value for each x inserted")
        for i in range(len(ins)):
            variables[ins[i]] = bool(insValues[i])
    else:
        b=len(line)
        if line.find("outputs", a, b):
            #Creation of the y set
            yLine = next(fin)
            ins = string.split(xLine, " ")
            for y in ins:
                outs [y] = None
            else:
                b=len(line)
                if line.find("begin", a, b):
                    #When the equations start we get to the next cicle which performs the calculations
                    break

#y = x + z
equation_XOR = re.compile(monomial + " = " + monomial + " \+ " + monomial + "|(0|1)")
#y = x * z
equation_AND = re.compile(monomial + " = " + monomial + " \* " + monomial + "|(0|1)")
#y = x
equation_ASSIGNEMENT = re.compile(monomial + " = " + monomial + "|(0|1)")

for line in fin:
    b=len(line)
    if line.find("end", a, b):
        break
    else:
        tmp = string.split(line, " ")
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
                y = xdict['x1'] * xdict['x2']
                variables[yAddr] = y
                if yAddr in outs:
                    outs[yAddr] = y
            else:
                if equation_ASSIGNEMENT.match(line):
                    yAddr = tmp[0]
                    xAddr = tmp[2]
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
                    raise Exception("equationReader: malformed equation " + line)

#Printing out the results
close(fin)
fout = open(sys.argv[2], "r")
for key, value in d.iteritems():
    fout.write(key + " = {}\n".format(value))

close(fout)
