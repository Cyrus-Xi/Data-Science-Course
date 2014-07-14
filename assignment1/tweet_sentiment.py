"""tweet_sentiment.py

Assignment 1
Twitter Sentiment Analysis in Python

Problem 2
Derive the sentiment of each tweet

Outputs a sentiment score for each tweet in provided file.
"""

import sys
import json


def get_sentiment_dict(sent_filename):
    """Create dict mapping words to sentiment score from provided
    filename.
    """
    with open(sent_filename, 'r') as infile:
        scores = {}
        for line in infile:
            term, score  = line.split("\t")  # Tab-delimited.
            scores[term] = int(score) 
        return scores

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

def calculate_tweets_score(input_name, sentiment_dict):
    """Print sentiment score for each tweet in provided
    file.
    """
    with open(input_name, 'r') as infile:
        for index, line in enumerate(infile):
            line_dict = json.loads(line)
            line_dict = convert(line_dict)
            # If no text value, return empty string.
            text_value = line_dict.get('text', '')
            #print "Tweet {} has this text: {}\n".format(index, text_value)
            tweet_sentiment = 0
            # Iterate over each term in text field.
            for term in text_value.split():
                #print term
                # If term isn't in sentiment dict, return score of 0.
                term_score = sentiment_dict.get(term, 0)
                tweet_sentiment += term_score
            print tweet_sentiment
            #print "Tweet {} has this sentiment score: {}\n".format(index, tweet_sentiment)

def main():
    sent_file = sys.argv[1]
    tweet_filename = sys.argv[2]
    word_sentiment_dict = get_sentiment_dict(sent_file)
    calculate_tweets_score(tweet_filename, word_sentiment_dict)

if __name__ == '__main__':
    main()
