#!/usr/bin/python
# -*- coding: utf-8 -*-

#import pudb; pu.db
import types
import math
import collections
from collections import namedtuple

Item = namedtuple('Item', ['value', 'weight', 'index'])
#1 - taken, -1 - not taken, 0 - not decided
taken = []
realIndex = []
items = []
capacity = 0
answerLine = ""

def decideIfTaken(value):
    if value == 1:
        return '1'
    else:
        return '0'

def formAnswer():
    line = ""
    line += decideIfTaken(taken[realIndex[0]])
    for i in xrange(1, itemsCount):
        line = line + ' ' + decideIfTaken(taken[realIndex[i]])  
    return line

def formRealIndex():
    for i in xrange(0, itemsCount):
        for j in xrange(0, itemsCount):
            if items[i].index == j:
                realIndex[j] = i
                break

def goodRate(item1, item2):
    rate1 = item1.value/float(item1.weight) 
    rate2 = item2.value/float(item2.weight)
    order = -1; #-1 highest rate first
    if rate1 > rate2:
        return order
    elif rate1 < rate2:
        return -order
    else:
        return 0

def calcFraction(capacity, index):
    global items
    return math.ceil(items[index].value*capacity/items[index].weight)

def calcEstimate(index, value, weight):
    global capacity
    global itemsCount
    global taken
    global items

    estimate = value
    capac = capacity - weight
    i = index
    while i < itemsCount and capac > 0:
        if taken[i] == 1:
            estimate += items[i].value
            capac -= items[i].weight

        elif taken[i] == 0:
            if capac >= items[i].weight:
                estimate += items[i].value
                capac -= items[i].weight
            else:
                estimate += calcFraction(capac, i) 
                capac = 0
        i += 1
    return estimate

stack = []
size = 0
optimalValue = 0

def pop():
    global stack, taken, size
    value = stack.pop()
    taken[size - 1] = 0
    size -= 1
    return value


def push(value):
    global stack, taken, size
    stack.append(value)
    size += 1
    taken[size - 1] = value

def notTooHeavy(weight, index, capacity):
    global items
    w = items[index].weight
    if weight + w <= capacity:
        return True
    else:
        return False

def addItem(index, value, weight):
    global optimalValue
    global items
    global answerLine
    v = items[index].value
    w = items[index].weight
    if value + v > optimalValue:
        optimalValue = value + v
        answerLine = formAnswer()    
    return value + v, weight + w 

def remItem(index, value, weight):
    global items
    return value - items[index].value, weight - items[index].weight

def solveWoRecursion():
    global capacity
    global itemsCount
    global taken
    global items
    global stack
    global size
    weight = 0
    value = 0
    estimateValue = 10000000
    for i in xrange(0, itemsCount):
        if notTooHeavy(weight, i, capacity):
            push(1)
            value, weight = addItem(i, value, weight)
            break
        else:
            push(-1)
    while size != 0:
        #print stack
        estimateValue = calcEstimate(size, value, weight)
        while estimateValue > optimalValue and size < itemsCount:
            if notTooHeavy(weight, size, capacity):
                push(1)
                value, weight = addItem(size - 1, value, weight) 
            else:
                push(-1)
            estimateValue = calcEstimate(size, value, weight)
        #if size == itemsCount:
            #showAll()
        if size > 0:
            cur = pop()
        while cur != 1 and size > 0:
            cur = pop()
        #viskas į dešinę buvo išnagrinėta
        if cur == 1:
            value, weight = remItem(size, value, weight)
            push(-1)

#def solve(itemIndex, value, weight):
    #global capacity
    #global itemsCount
    #global bestValue
    #global answerLine
    #estimate = 0
    #w = items[itemIndex].weight
    #v = items[itemIndex].value
    #for j in xrange(1, -2,  -2):
        #if j == 1 and weight + w <= capacity:

            #taken[itemIndex] = j
            #estimate = calcEstimate()
            ##print 'item: ', itemIndex, ' decision: ', j, 'estimate: ', estimate, ' bestValue: ', bestValue
            #if value + v > bestValue:
                #bestValue = value + v
                #answerLine = formAnswer()                
                ##printTaken()
            #if estimate > bestValue and itemIndex + 1 < itemsCount:
                #solve(itemIndex + 1, value + v, weight + w)
            #taken[itemIndex] = 0
        #elif j == -1:
            #taken[itemIndex] = j
            #estimate = calcEstimate()
            ##print 'item: ', itemIndex, ' decision: ', j, 'estimate: ', estimate, ' bestValue: ', bestValue
            #if estimate > bestValue and itemIndex + 1 < itemsCount:
                #solve(itemIndex + 1, value, weight)
            #taken[itemIndex] = 0


def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    
    global itemsCount 
    global bestValue
    global capacity
    global answerLine
    
    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    itemsCount = int(firstLine[0])
    capacity = int(firstLine[1])
    estimateCapacity = capacity
    value = 0

    for i in range(1, itemsCount+1):
        taken.append(0)
        line = lines[i]
        parts = line.split()
        items.append(Item(int(parts[0]), int(parts[1]), int(i - 1)))
        realIndex.append(0)
    #sort highest ratio first
    items.sort(cmp=goodRate)
    formRealIndex()
    #for i in range(0, itemsCount):
        #print items[i].value, items[i].weight, items[i].index
    #solve(0, 0, 0)
    solveWoRecursion() 
    value = optimalValue
    # prepare the solution in the specified output format
    outputData = str(value) + ' ' + str(1) + '\n'
    outputData += answerLine
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

