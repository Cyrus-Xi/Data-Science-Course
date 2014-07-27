"""inverted_index.py
Assignment 3
Algorithms in MapReduce

Problem 1
Create an inverted index.

Outputs each unique word with the list of document IDs 
in whose documents it appears.
"""

import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    words = value.split()
    for w in words:
      mr.emit_intermediate(w, key)

def reducer(key, list_of_values):
    # key: word
    # value: document IDs
    list_ids = []
    for doc_id in list_of_values:
      list_ids.append(doc_id)
    # Take out duplicates.
    list_ids = list(set(list_ids))
    mr.emit((key, list_ids))


if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
