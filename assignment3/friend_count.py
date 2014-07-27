"""friend_count.py
Assignment 3
Algorithms in MapReduce

Problem 3
Describe a MapReduce algorithm to count the number of friends
for each person in a simple social network dataset.

Outputs a pair (person, friend_count) where person 
is a string and friend_count is an integer indicating the 
number of friends associated with person.
"""

import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    # key: person's name
    # value: 1, for one friend
    key = record[0]
    value = 1
    mr.emit_intermediate(key, value)

def reducer(key, values):
    # key: person's name
    # value: list of 1's, one for each friend
    total = 0
    for v in values:
      total += v
    mr.emit((key, total))


if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
