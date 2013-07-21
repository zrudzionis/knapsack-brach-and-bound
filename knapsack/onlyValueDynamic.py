#!/usr/bin/python
# -*- coding: utf-8 -*-


def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    items = int(firstLine[0])
    capacity = int(firstLine[1])

    values = []
    weights = []

    for i in range(1, items+1):
        line = lines[i]
        parts = line.split()

        values.append(int(parts[0]))
        weights.append(int(parts[1]))

    items = len(values)

    value = 0;
    
    #for i in xrange(0, items):
        #print (values[i], weights[i])

    taken = [ 0 for i in range(1, items + 1) ]
    table = [ [0 for i in range(0, capacity + 1)] for j in xrange(2) ]
   
    #print table

    curRow = 0;
    for i in xrange(1, items + 1):
        for j in xrange(1, capacity + 1):
            itemIndex = i - 1;
            if weights[itemIndex] <= j:
                table[curRow][j] = max(table[not curRow][j - weights[itemIndex]]
                        + values[itemIndex],
                        table[not curRow][j])
            else:
                table[curRow][j] = table[not curRow][j]
        curRow = not curRow
    value = table[not curRow][capacity] 

    # prepare the solution in the specified output format
    outputData = str(value) + ' ' + str(1) + '\n'
    #outputData += ' '.join(map(str, taken))
    return outputData


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'


