# word_count.py
# ===================================================
# Implement a word counter that counts the number of
# occurrences of all the words in a file. The word
# counter will return the top X words, as indicated
# by the user.
# ===================================================

import re
from hash_map import HashMap

"""
This is the regular expression used to capture words. It could probably be endlessly
tweaked to catch more words, but this provides a standard we can test against, so don't
modify it for your assignment submission.
"""
rgx = re.compile("(\w[\w']*\w|\w)")


def hash_function_2(key):
    """
    This is a hash function that can be used for the hashmap.
    """

    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


def top_words(source, number):
    """
    Takes a plain text file and counts the number of occurrences of case insensitive words.
    Returns the top `number` of words in a list of tuples of the form (word, count).

    Args:
        source: the file name containing the text
        number: the number of top results to return (e.g. 5 would return the 5 most common words)
    Returns:
        A list of tuples of the form (word, count), sorted by most common word. (e.g. [("a", 23), ("the", 20), ("it", 10)])
    """

    keys = set()

    ht = HashMap(2500, hash_function_2)

    # This block of code will read a file one word as a time and  |
    # put the word in `w`. It should be left as starter code.     |
    with open(source) as f:                                     # |
        for line in f:                                          # |
            words = rgx.findall(line)                           # |
            for w in words:                                     # |
                # lower case all incoming words to make case insensitive
                w = w.lower()
                # Check if hashtable already contains word
                if ht.contains_key(w):
                    # If so retrieve the count for the given word
                    count = ht.get(w)
                    # Update existing key with incremented count value
                    ht.put(w, count + 1)
                else:
                    # Add new word to keys set collection
                    keys.add(w)
                    # put new word in hash table with a count of 1
                    ht.put(w, 1)
                # Check if table load is over load limit before next word
                if ht.table_load() > 8:
                    # if so, resize hash table to twice the capacity
                    ht.resize_table(2 * ht.capacity)
    # initialize tuple word/count list
    topWords = []
    # for each key in the set of keys
    for key in keys:
        # append the key and value as a tuple in the topWords list
        topWords.append((key, ht.get(key)))
    # once all tuples are added to list, sort list by the count of each key in descending order
    topWords.sort(key=lambda keyCountTup: keyCountTup[1], reverse=True)
    # After sort, set top word list to only contain the given number of tuples requested
    topWords = topWords[:number]
    # return topWords list of tuples of length equal to number
    return topWords
