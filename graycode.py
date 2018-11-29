# -*- coding: utf-8 -*-
import random

CONFIG_N    = 10
CONFIG_M    = 20
COUNTER     = 0
EXPERIMENTS = 10

def generate_record_file(filename, count=10000):
    """ generate random record file given generation parameters """
    with open(filename, 'w') as output:
        # generate 10K sample records
        for _ in range(count):
            output.write(','.join([str(random.randint(1, CONFIG_N)) for _ in range(CONFIG_M)]))
            output.write('\n')

def load_record_file(filename):
    """ load record file from disk """
    data = []
    with open(filename) as input:
        # load input data line by line
        for line in input:
            # create lists of list
            data.append([x for x in map(int, line.split(','))])
    return data

def calculate_full_score(data):
    """ calculate full score of data """
    score = 0
    # to calculate full score we iterate over all records and calculate
    # absolute distance between each adjacent record
    for i in range(1, len(data)):
        for j in range(CONFIG_M):
            score += abs(data[i][j] - data[i - 1][j])
    return score

def calculate_binary_score(data):
    """ calculate binary score of data """
    # to calculate full score we iterate over all records and count
    # number of records which are different
    score = 0
    for i in range(1, len(data)):
        for j in range(CONFIG_M):
            score += int(data[i][j] != data[i - 1][j])
    return score

def gray_order():
    """ gray ordering """
    def mycmp(record_a, record_b):
        """ compare two records """
        i = 0
        total_d = 0
        global COUNTER

        # iterate over all entries of these records and find the point it doesn't match
        while i < CONFIG_M:
            if record_a[i] != record_b[i]:
                break
            total_d += record_a[i]
            i += 1
            COUNTER += 1

        # return -1, 0 or 1
        if total_d % 2 == 0:
            return (record_a[i] - record_b[i])
        return (record_b[i] - record_a[i])

    # comparator class required in python3.5+
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

def gray_rank(record):
    """ calculate rank for sorting """
    global COUNTER

    # calculate rank based on Homer's rule
    rank = record[0]
    for i in range(CONFIG_M):
        temp = CONFIG_N - record[i] - 1
        if i % 2 == 0:
            temp = record[i]
        rank = rank * CONFIG_N + temp
        COUNTER += 1
    return rank

def radix_sort(data):
    """ radix sort or records """
    global COUNTER

    # Radix sorting
    original_list = data
    for j in reversed(range(CONFIG_M)):

        # create a new list (one for each radix)
        newlist = []
        for _ in range(CONFIG_N):
            newlist.append([])

        # iterate over original list
        for record in original_list:
            # bucket sort the records and put them in list
            if record[j] % 2 == 0:
                newlist[record[j] - 1].append(record)
            else:
                newlist[record[j] - 1].insert(0, record)
            COUNTER += 1

        # update original list
        original_list = []
        for i in range(CONFIG_N):
            original_list.extend(newlist[i])

    # return original list
    return original_list

if __name__ == '__main__':

    for i in range(EXPERIMENTS):
        random.seed(i)

        print('=========== EXPERIMENT %d ===========' % (i + 1))

        # generate record file
        print('Generating record file...')
        generate_record_file('record_%d.txt' % i)

        # load record file
        print('Loading record file...')
        data = load_record_file('record_%d.txt' % i)

        # calculate score
        print('Full Score:', calculate_full_score(data))
        print('Binary Score:', calculate_binary_score(data))

        # gray ordering
        print('Gray Ordering...')
        COUNTER = 0     # reset counter
        data_sorted = sorted(data, key=gray_order())
        print('\tCounter:', COUNTER)
        print('\tFull Score:', calculate_full_score(data_sorted))
        print('\tBinary Score:', calculate_binary_score(data_sorted))

        # rank method
        print('Rank Method...')
        COUNTER = 0     # reset counter
        data_sorted = sorted(data, key=gray_rank)
        print('\tCounter:', COUNTER)
        print('\tFull Score:', calculate_full_score(data_sorted))
        print('\tBinary Score:', calculate_binary_score(data_sorted))

        # radix sorting
        print('Radix Sorting...')
        COUNTER = 0     # reset counter
        data_sorted = radix_sort(data)
        print('\tCounter:', COUNTER)
        print('\tFull Score:', calculate_full_score(data_sorted))
        print('\tBinary Score:', calculate_binary_score(data_sorted))

        print()
