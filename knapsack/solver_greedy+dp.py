#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import math as math
from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')
    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []
    values = []
    weights = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        ''' items.append(Item(i-1, int(parts[0]), int(parts[1])))'''
        values.append(int(parts[0]))
        weights.append(int(parts[1]))
    # a trivial algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full

    value = 0
    weight = 0
    taken = [0]*len(values)
    # In the simple case we can use greedy algorithm
    '''
    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
    '''
    # If we get big capacity we should use float numbers to find approximate solution
    if ((item_count > 100)&(item_count <= 2000) & (capacity > 200000)):
        capacity = math.floor(capacity / 100)
        weights = [math.ceil(x / 100) for x in weights]
    # Another case: use dynamic programming to find the EXACT solution
    if((item_count<=2000)):
        dynamic = np.zeros((item_count + 1, capacity + 1))
        for i in range(1, item_count + 1, 1):
            for k in range(capacity + 1):
                if (weights[i - 1] <= k):
                    dynamic[i][k] = max(dynamic[i - 1][k], dynamic[i - 1][k - weights[i - 1]] + values[i - 1])
                else:
                    dynamic[i][k] = dynamic[i - 1][k]
        k = capacity
        i = item_count
        while (i != 0):
            if (dynamic[i][k] == dynamic[i - 1][k - weights[i - 1]] + values[i - 1]):
                taken[i - 1] = 1
                value += values[i - 1]
                k = k - weights[i - 1]
                i = i - 1
            else:
                i = i - 1
    # The final case: if we have the large number of items we should use greedy.
    else:
        average_value = list(np.array(values)/np.array(weights))
        while (True) :
            max_value = max(average_value)
            if (max_value < 0.1):
                break
            max_index = average_value.index(max_value)
            if weight + weights[max_index] <= capacity:
                taken[max_index] = 1
                value += values[max_index]
                weight += weights[max_index]
            average_value[max_index] = 0

        '''
        for i in range(len(values)):
            if weight + weights[i] <= capacity:
                taken[i] = 1
                value += values[i]
                weight += weights[i]
        '''

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

