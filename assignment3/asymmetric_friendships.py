"""friend_count.py
Assignment 3
Algorithms in MapReduce

Problem 4
Generate a list of all asymmetric friend relationships 
in a simple social network dataset.

For each (person, friend) relationship that is asymmetric, 
output both (person, friend) and (friend, person).
"""

import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    # key: friend relationship tuple
    # value: marker for symmetry

    # First (given) direction.
    key = (record[0], record[1])
    value = 1
    mr.emit_intermediate(key, value)

    # Other (reversed) direction.
    key = (record[1], record[0])
    value = -1
    mr.emit_intermediate(key, value)


def reducer(key, values):
    # key: friend relationship tuple
    # value: list of symmetry markers
    total = 0
    for v in values:
      total += v

    # If total is 0, then symmetric and don't emit.
    if total == -1 or total == 1:
      mr.emit(key)


if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
