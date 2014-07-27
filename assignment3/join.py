"""join.py
Assignment 3
Algorithms in MapReduce

Problem 2
Implement a relational join as a MapReduce query.

Outputs a joined record: a single list that 
contains the attributes from the order record 
followed by the fields from the line item record.
"""

import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    # key: element being joined on, i.e. the order ID
    # value: the whole tuple
    key = record[1]  # Second element in each record is order_id.
    value = record  # Don't have to remove key.
    mr.emit_intermediate(key, value)

def reducer(key, records):
    # key: element being joined on
    # value: all the records with that shared key

    # Separate relations.
    item_records = [rec for rec in records if rec[0] == 'line_item']
    order_records = [rec for rec in records if rec[0] == 'order']
    
    # Do cross product.
    for o_rec in order_records:
      for i_rec in item_records:
        output_rec = o_rec + i_rec
        mr.emit(output_rec)


if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
