"""friend_count.py
Assignment 3
Algorithms in MapReduce

Problem 6
Design a MapReduce algorithm to compute the matrix multiplication A x B.

A and B are sparse matrices where each record is of form (i, j, value).
"""

import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    # key: output table entry position
    # value: the "missing" other dimension and the value itself
    table = record[0]
    row = record[1]
    col = record[2]
    val = record[3]

    # Hard-coded matrix dimensions to maintain scalability.
    # Could scan input for dimensions but would take two
    # map-reduces or would need shared memory.
    for k in range(0, 5):
      if table == 'a':
        mr.emit_intermediate((row, k), (col, val))
      elif table == 'b':
        mr.emit_intermediate((k, col), (row, val))


def reducer(key, values):
    # key: output table entry position
    # values: the values themselves and indices

    # Sort for easier computation.
    values.sort()  # In-place sort
    total = 0
    # Iterate pairwise through list looking for, e.g., 
    # (0, 24) and (0, 13) and multiply the two.
    for curr_entry, next_entry in zip(values, values[1:]):
      if curr_entry[0] == next_entry[0]:
        product = curr_entry[1] * next_entry[1]
        # Sum products for the dot product.
        total += product

    return_tuple = (key[0], key[1], total)
    mr.emit(return_tuple)


if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
