"""unique_trims.py
Assignment 3
Algorithms in MapReduce

Problem 5
Write a MapReduce query to remove the last 10 characters 
from each string of nucleotides, then remove any duplicates 
generated.

Outputs the unique trimmed nucleotide strings.
"""

import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    # key: nucleotide string
    # value: ID
    key = record[1][:-10] # Trim string.
    value = record[0]
    mr.emit_intermediate(key, value)


def reducer(key, value):
    # Can just emit key directly to maintain
    # uniqueness.
    mr.emit(key)


if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
