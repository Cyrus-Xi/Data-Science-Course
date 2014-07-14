"""top_ten.py
Assignment 1
Twitter Sentiment Analysis in Python

Problem 6
Top ten hash tags

Outputs the top ten most frequently occuring hashtags with their frequency.
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
    """Create dict mapping each unique hashtag to its frequency."""
    freq_hashtag_dict = {}
    with open(input_name, 'r') as infile:
        for index, line in enumerate(infile):
            line_dict = json.loads(line)
            line_dict = convert(line_dict)
            # If no entities value, return empty string.
            entities = line_dict.get('entities', '')
            if entities:
                list_hashtags = entities.get('hashtags', [])
                #print list_hashtags
                for hashtag_obj in list_hashtags:
                    hashtag = hashtag_obj['text']
                    # If hashtag not already in dict, initialize to 1.
                    freq_hashtag_dict[hashtag] = freq_hashtag_dict.get(hashtag, 0) + 1 
    return freq_hashtag_dict

def get_top_ten(input_dict):
    """Use lambda expression to reverse sort and get the top ten 
    most frequently occurring hashtags.
    """
    top_ten_hashtags = sorted(input_dict.iteritems(), key=lambda k:-k[1])[:10]
    return top_ten_hashtags

def output_freq_list(input_list):
    """Print each top 10 hashtag with its frequency."""
    for item in input_list:
        print "{} {}".format(item[0], item[1])

def main():
    tweet_filename = sys.argv[1]
    freq_dict = create_freq_dict(tweet_filename)
    top_hashtags = get_top_ten(freq_dict)
    output_freq_list(top_hashtags)

if __name__ == '__main__':
    main()
