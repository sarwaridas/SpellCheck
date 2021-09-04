import time
import re
import numpy as np


def createADictionary(filename):
    # Reads txt file (Input exact path of file!)
    # Returns dictionary of all words contained in the file
    word_dict = dict()
    with open(filename, "r") as f:
        for line in f:
            for word in line.strip("\n,.:;-'").lower().split(" "):
                if word not in word_dict:
                    word_dict[word] = 1
                else:
                    word_dict[word] += 1
    return word_dict


with open("referenceDict.txt", "r") as f:
    referenceList = [i for j in f for i in j.split()]

referenceList1 = np.array(referenceList)
austenDict = createADictionary("Austen_trial.txt")


def calculateEditDistance(source, target):
    # print(target)
    n = len(source)
    m = len(target)
    source = " " + source
    # print(source)
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


def getReplaceWord(string1, reference=referenceList1):
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
    pattern = '(^[^A-Z0-90-9.,;""?():-_][^A-Z0-9.,;""?():-_]+)'
    if re.fullmatch(pattern, str):
        return True
    else:
        return False


for key, value in austenDict.items():
    if (keepThis(key) == True) and (key not in referenceList):
        austenDict[key] = getReplaceWord(key)


with open("Austen_trial.txt", "r") as f:
    data = f.read().replace("\n", " ").split(" ")
    final_list = " "
    for word in data:
        if word == "":
            pass
        elif (
            re.findall(r"\w+", word)[0] in austenDict.keys()
            and type(austenDict[re.findall(r"\w+", word)[0]]) == str
        ):  ##figure out a way to preserve punctuation
            final_list = final_list + austenDict[re.findall(r"\w+", word)[0]] + " "
        else:
            final_list = final_list + word + " "

print(final_list)
