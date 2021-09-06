"""
Build from scratch a spelling corrector in Python. It should include:
1. tokenization
2. Levenshtein distance-based non-word spelling correction
3. de-tokenization

As an example use case, consider a version of Jane Austen’s Sense and Sensibility (available via nltk’s gutenberg corpus) corrupted by random insertions,
deletions, and substitutions. See for reference gen_corrupted.py.
Your spelling correction function:
• should accept a document as a single string and return the corrected
document as a single string.
• may use only standard libraries and numpy.
• may use this reference word list [https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english.txt]
 English word list, which is ordered by decreasing frequency

"""

from os import PRIO_PGRP
import time
import re
import numpy as np


def createADictionary(filename):
    """
    Reads txt file and returns dictionary of all words contained
    in that file, with their frequency [tokenization]
    """
    word_dict = dict()
    with open(filename, "r") as f:
        for line in f:
            for word in line.strip("\n,.:;-'").lower().split(" "):
                if word.strip("\n,.:;-'") not in word_dict:
                    word_dict[word.strip("\n,.:;-'")] = 1
                else:
                    word_dict[word.strip("\n,.:;-'")] += 1
    return word_dict


with open(
    "referenceDict.txt", "r"
) as f:  # Creating a dictionary of reference word list
    referenceList = [i for j in f for i in j.split()]

referenceList = np.array(referenceList)
austenDict = createADictionary(
    "Austen_trial.txt"
)  # Creating a dictionary of words in Jane Austen's Sense & Sensibility


def calculateEditDistance(source, target):
    """
    calculates Levenshtein based edit distance
    between a source and target variable
    """
    n = len(source)
    m = len(target)
    source = " " + source
    target = " " + target
    D = [[0 for i in range(m + 1)] for j in range(n + 1)]
    # Initialization:the zeroth column is the distance from the empty string
    for i in range(1, n + 1):
        D[i][0] = D[i - 1][0] + 1
    for j in range(1, m + 1):
        D[0][j] = D[0][j - 1] + 1
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if source[i] == target[j]:
                D[i][j] = D[i - 1][j - 1]
            elif source[i] != target[j]:
                D[i][j] = min([D[i - 1][j] + 1, D[i - 1][j - 1] + 1, D[i][j - 1] + 1])
    return D[i][j]


def getReplaceWord(string1, reference=referenceList):
    """
    From the reference list, for any given string, returns the words with the
    smallest Levenshtein based edit distance
    """
    replace = string1
    min_dist = len(string1)
    for i in range(len(referenceList) - 1):
        if calculateEditDistance(string1, referenceList[i]) < min_dist:
            replace = referenceList[i]
            min_dist = calculateEditDistance(string1, referenceList[i])
        else:
            pass
    return replace


def keepThis(str):
    """
    In my code, I don't attempt to correct proper nouns or any words that have a
    capitalized first letter, unless they are preceded by a period (indicating that they are
    the start of a sentence). This function returns a True for words I am attempting correct
    and False if I am skipping over correction

    """
    pattern = '(^[^A-Z0-90-9.,;""?():-_][^A-Z0-9.,;""?():-_]+)'
    # pattern = "(^[^A-Z0-90-9.,;?():-_][^A-Z0-9.,;?():-_]+)|[.][A-Z].+"
    if re.fullmatch(pattern, str):
        return True
    else:
        return False


# using keepThis to check if I am attempting to correct the word
# using the referenceList to check if the word is already valid, in which case I skip over it
# finding the replacement word with least edit distance using getReplaceWord()

for key, value in austenDict.items():

    if (keepThis(key) == True) and (key not in referenceList):
        austenDict[key] = getReplaceWord(key)

# creating a list of all corrupted words
corruptedAustenList = np.array([])
for key, values in austenDict.items():
    if key.strip("\n,.:;-'") not in referenceList:
        corruptedAustenList = np.append(corruptedAustenList, key.strip("\n,.:;-'"))

# preserving the punctuation for each corrupted word to instert after replacement
def keepPunc(x):
    if len(re.findall(r"[?!,.;:]$", x)) > 0:
        return re.findall(r"[?!,.;:]$", x)[0]
    else:
        return ""


# reading trial text and replacing corrupted words with replacement words
# performing de-tokenization and saving corrected text in 'final_list'
with open("Austen_trial.txt", "r") as f:
    # data = f.read().replace("\n", " ").split(" ")
    data = f.read().replace("\n", " ")
    final_list = " "
    for i in data.split(" "):
        if (
            i.strip("\n,.:;'") in corruptedAustenList
            and len(re.findall(r"\w", i)) != 0
            and re.findall(r"\w+", i)[0] in austenDict.keys()
            and type(austenDict[re.findall(r"\w+", i)[0]]) != int
        ):
            final_list = (
                final_list
                + austenDict[re.findall(r"\w+", i.strip("\n,.:;'"))[0]]
                + keepPunc(i)
                + " "
            )
        else:
            final_list = final_list + i + " "

# writing corrected text to "Austen_trial_corrected.txt"
with open("Austen_trial_corrected.txt", "w") as stream:
    stream.write(final_list)
