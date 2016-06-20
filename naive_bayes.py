# -*- coding: utf-8 -*-

__author__ = "Rogers de Pelle"
__contact__ = "@rogersdepelle"

from math import log, exp


def learn(docs, values):
    """
        docs: Set of text documents along with their target values;
        values: Set of all possible target values;
    """

    n_docs = 0
    probabilities = {}
    vocabulary = set()

    for value in values:
        vocabulary |= set(' '.join(docs[value]).split())
        n_docs += len(docs[value])

    for value in values:
        probabilities[value] = {}
        probabilities[value]['prob'] = len(docs[value])/float(n_docs)
        text = ' '.join(docs[value]).split()
        n_words = len(text)
        probabilities[value]['words'] = {}
        for word in vocabulary:
            n_times = text.count(word)
            probabilities[value]['words'][word] = float(n_times + 1) / (n_words + len(vocabulary))

    return probabilities, vocabulary


def classify(doc, probabilities, vocabulary, values):
    """
        probabilities: Dict with words probalities
        vocabulary: All distinct words in training text
    """
    old_prob = float("-inf")
    result = ""

    words = set(doc.split()).intersection(vocabulary)
    for value in values:
        prob = 1
        for word in words:
            prob += log(probabilities[value]['words'][word])
        prob += log(probabilities[value]['prob'])
        if prob > old_prob:
         old_prob = prob
         result = value

    return result
