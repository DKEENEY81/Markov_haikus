#!/usr/bin/env python3

import sys
from string import punctuation
import pprint
import json
from nltk.corpus import cmudict

cmudict = cmudict.dict()


def main():
    haiku = loader('train.txt')
    exceptions = not_in_dict(haiku)
    build_dict = input("\nManually build an exceptions dictionary (y/n)? \n")
    if build_dict.lower() == 'n':
        sys.exit()
    else:
        missing_words_dict = make_exceptions_dict(exceptions)
        save_exceptions(missing_words_dict)


def loader(filename):
    # loads training data from file split into a set of individual words
    with open(filename) as f:
        training = set(f.read().replace('-', ' ').split())
        return training


def not_in_dict(words):
    # checks set of words and tracks those not found in cmudict (lowercases, removes 's and punctuation)
    not_found = set()
    for word in words:
        word = word.lower().strip(punctuation)
        if word.endswith("'s") or word.endswith("‘s"):
            word = word[:-2]
        if word not in cmudict:
            not_found.add(word)
    print("\nexceptions:")
    print(*not_found, sep='\n')
    print(f"\nNumber of unique words in training corpus: {len(words)}")
    print(f"\nNumber of words in training corpus not in CMUdict {len(not_found)}")
    membership = (1 - (len(not_found) / len(words))) * 100
    print(f"CMUdict membership = {membership:.1f}{'%'}")
    return not_found


def make_exceptions_dict(words_not_found):
    # Return dictionary of words and their syllable count from set of words using user input
    missing = {}
    print("Input # of syllables in word")
    for word in words_not_found:
        while True:
            sylls = input(f"Enter number of syllables in {word}:")
            if sylls.isdigit():
                break
            else:
                print("    Not a valid answer", file=sys.stderr)
        missing[word] = int(sylls)
    print()
    pprint.pprint(missing, width=1)
    print("\nMake changes before saving?")
    print("""
    0 - Exit and Save
    1 - Add word or change syllable count
    2 - Remove a word
    """)
    while True:
        choice = input('\nEnter choice:  ')
        if choice == 0:
            break
        elif choice == 1:
            word = input("\nWord to change? ")
            missing[word] = int(input(f'Enter number of syllables in {word}'))
        elif choice == 2:
            word = input("\nWord to delete?")
            missing.pop(word, None)
    print("\nNew words or changes: ")
    pprint.pprint(missing, width=1)

    return missing

def save_exceptions(dic_of_words):
    # converts dictionary of missing words to json, writes to new file, informs user
    j_string = json.dumps(dic_of_words)
    with open("missing_words.json", 'w') as f:
        f.write(j_string)
        f.close()
    print("\nFile saved as missing_words.json")

if __name__ == '__main__':
    main()
