"""frequency.py
Assignment 1
Twitter Sentiment Analysis in Python

Problem 4
Compute Term frequency

Outputs each unique term with its frequency in provided file.
"""

import sys
import json


def convert(input):
    """Recursively convert JSON input from unicode to byte strings."""
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def create_freq_dict(input_name):
    """Create dict mapping each unique term to its frequency."""
    freq_dict = {}
    with open(input_name, 'r') as infile:
        for index, line in enumerate(infile):
            line_dict = json.loads(line)
            line_dict = convert(line_dict)
            # If no text value, return empty string.
            text_value = line_dict.get('text', '')
            #print "Tweet {} has this text: {}\n".format(index, text_value)
            # Iterate over each term in text field.
            for term in text_value.split():
                #print term
                # If term not in dict, initialize value to 1.
                freq_dict[term] = freq_dict.get(term, 0) + 1
    return freq_dict

def output_freq_dict(input_dict):
    """Print each term with its frequency."""
    for key in input_dict:
        print "{} {}".format(key, input_dict[key])

def main():
    tweet_filename = sys.argv[1]
    freq_dict =  create_freq_dict(tweet_filename)
    output_freq_dict(freq_dict)

if __name__ == '__main__':
    main()
