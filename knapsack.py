
import numpy as np

def read_numbers(data_file):
    input_data_file = open(data_file, 'r')
    input_data = input_data_file.readlines()
    input_data_file.close()

    numbers = np.array([])
    for i_line in xrange(len(input_data)):
        entries = input_data[i_line].split()
        entries = filter(None, entries) # remove empty entries
        line_numbers = [ float(x) if x.lower != "inf" else float("inf") for x in entries ]
        numbers = np.append(numbers, line_numbers)
    return numbers

def read_data(data_file):
    numbers = read_numbers(data_file)
    cur_entry = 0

    # number of nodes
    num_items = int(numbers[cur_entry])
    cur_entry += 1
    
    # maximum capacity of the knapsack
    capacity = int(numbers[cur_entry])
    cur_entry += 1
    
    # get data on the items
    value = np.zeros(num_items, dtype = 'int')
    size = np.zeros(num_items, dtype = 'int')
    for i_item in xrange(num_items):
        value[i_item] = float(numbers[cur_entry])
        cur_entry += 1
        size[i_item] = float(numbers[cur_entry])
        cur_entry += 1
        
    return value, size, capacity

def make_dummy_solution(value, size, capacity):
    num_items = len(value)
    solution_value = 0
    solution_items = np.zeros(num_items, 'int')
    
    table = [[0 for w in xrange(capacity + 1)] for j in xrange(num_items + 1)]
 
    for j in xrange(1, num_items + 1):
        for w in xrange(1, capacity + 1):
            table[j][w] = table[j-1][w]
            if w >= size[j-1] and table[j][w] < table[j-1][w - size[j-1]] + value[j-1]:
                table[j][w] = table[j-1][w - size[j-1]] + value[j-1]
 
    solution_value = table[num_items][capacity]
    w = capacity
    
    for j in xrange(num_items, 0, -1):
        if table[j][w] != table[j-1][w]:
            solution_items[j-1] = 1
            w -= size[j-1]    
    
    return solution_value, solution_items

import sys
import os

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        value, size, capacity = read_data(file_location)
        out_file_path = os.path.splitext(file_location)[0] + "_solution.txt"

        solution_value, solution_items = make_dummy_solution(value, size, capacity)
        
        print solution_value
        print ' '.join(map(str, solution_items))

        with open(out_file_path,'w') as f:
            f.write(str(solution_value) + "\n")
            for i in xrange(len(solution_items)):
                if i+1 != (len(solution_items)):
                    f.write(str(solution_items[i]) + " ")
                else:
                    f.write(str(solution_items[i]))        
        
    else:
        print 'This script requires an input file as command line argument.'

    
