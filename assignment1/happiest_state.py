"""happiest_state.py
Assignment 1
Twitter Sentiment Analysis in Python

Problem 5
Which State is happiest?

Outputs the state with the highest average tweet sentiment.
"""

import sys
import json

# Map state abbreviations to state names.
ABBREV_TO_STATE = {
'AK': 'alaska',
'AL': 'alabama',
'AR': 'arkansas',
'AZ': 'arizona',
'CA': 'california',
'CO': 'colorado',
'CT': 'connecticut',
'DE': 'delaware',
'FL': 'florida',
'GA': 'georgia',
'HI': 'hawaii',
'IA': 'iowa',
'ID': 'idaho',
'IL': 'illinois',
'IN': 'indiana',
'KS': 'kansas',
'KY': 'kentucky',
'LA': 'louisiana',
'MA': 'massachusetts',
'MD': 'maryland',
'ME': 'maine',
'MI': 'michigan',
'MN': 'minnesota',
'MO': 'missouri',
'MS': 'mississippi',
'MT': 'montana',
'NC': 'north carolina',
'ND': 'north dakota',
'NE': 'nebraska',
'NH': 'new hampshire',
'NJ': 'new jersey',
'NM': 'new mexico',
'NV': 'nevada',
'NY': 'new york',
'OH': 'ohio',
'OK': 'oklahoma',
'OR': 'oregon',
'PA': 'pennsylvania',
'RI': 'rhode island',
'SC': 'south carolina',
'SD': 'south dakota',
'TN': 'tennessee',
'TX': 'texas',
'UT': 'utah',
'VA': 'virginia',
'VT': 'vermont',
'WA': 'washington',
'WI': 'wisconsin',
'WV': 'west virginia',
'WY': 'wyoming'
}

# Also create reverse dict to go both directions.
# State names mapped to state abbreviations.
STATE_TO_ABBREV = {v:k for k, v in ABBREV_TO_STATE.items()}

# Create lists of states and abbreviations by themselves for 
# convenience.
LIST_STATES = [v.lower() for k, v in ABBREV_TO_STATE.items()]
LIST_ABBREVS = [k for k, v in ABBREV_TO_STATE.items()]

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

def get_sentiment_by_state(input_name, sentiment_dict):
    """Create dict mapping each state to its tweets' total
    sentiment and count.
    """
    state_sentiment_dict = {}
    for state in LIST_STATES:
        # Map each state to list of total sentiment score and number of
        # applicable tweets.
        state_sentiment_dict[state] = [0, 0]
    with open(input_name, 'r') as infile:
        for index, line in enumerate(infile):
            line_dict = json.loads(line)
            line_dict = convert(line_dict)
            state_location = get_state_location(line_dict)
            #print state_location
            # Ensure tweet has needed location information.
            if state_location:
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
                #print tweet_sentiment
                # Add tweet sentiment.
                state_sentiment_dict[state_location][0] += tweet_sentiment
                # Add 1, so can later compute average.
                state_sentiment_dict[state_location][1] += 1
                #print "Tweet {} has this sentiment score: {}\n".format(index, tweet_sentiment)
    return state_sentiment_dict

def get_state_location(input_dict):
    """Test if tweet has user location field with state name.
    If so, return the state. Else implicitly return None.
    """
    user_data = input_dict.get('user', '')
    # User field has stuff inside.
    if user_data:
        # Get location data.
        location = user_data.get('location', '')
        # Look for either full state name or all-caps state
        # abbreviation.
        for state in LIST_STATES:
            if state in location.lower():
                return state
        for abbrev in LIST_ABBREVS:
            if abbrev in location:
                return ABBREV_TO_STATE[abbrev]

def get_average_sentiment_by_state(input_dict):
    """Create new dict mapping state to average tweet sentiment score."""
    # Only do average if there was at least 1 applicable tweet; otherwise would divide
    # by 0.
    average_sentiment_dict = {k:v[0]/v[1] for k, v in input_dict.items() if v[1] != 0}
    return average_sentiment_dict

def get_happiest_state(input_dict):
    """Return the state with the highest average sentiment score."""
    # Use lambda expression to compare states based on their average tweet sentiment.
    happiest_state = max(input_dict.iterkeys(), key=(lambda k: input_dict[k]))
    return STATE_TO_ABBREV[happiest_state]

def main():
    sent_file = sys.argv[1]
    tweet_filename = sys.argv[2]
    word_sentiment_dict = get_sentiment_dict(sent_file)
    naive_sentiment_by_state = get_sentiment_by_state(tweet_filename, word_sentiment_dict)
    average_sentiment_by_state = get_average_sentiment_by_state(naive_sentiment_by_state)
    print get_happiest_state(average_sentiment_by_state)

if __name__ == '__main__':
    main()
