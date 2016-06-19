# -*- coding: utf-8 -*-

__author__ = "Rogers de Pelle"
__contact__ = "@rogersdepelle"


def learn(docs, values):
    """
        docs: Set of text documents along with their target values;
        values: Set of all possible target values;
    """

    n_docs = 0
    probabilities = {}
    vocabulary = set()

    #collect all distinct words, punctuation, and other tokens
    for value in values:
        vocabulary |= set(' '.join(docs[value]).split())
        n_docs += len(docs[value])

    #calculate the probabilities
    for value in values:
        probabilities[value] = {}
        probabilities[value]['prob'] = len(docs[value])/float(n_docs)
        text = ' '.join(docs[value]).split()
        n_words = len(text)
        probabilities[value]['words'] = {}
        for word in vocabulary:
            n_times = text.count(word)
            probabilities[value]['words'][word] = float(n_times + 1) / (n_words + len(vocabulary))

    print probabilities


def classify():
    """
    #all words in Doc that contain tokens found in Vocabulary
    positions = doc.split intersection vocabulary
    v = 0
    for value in values
        probabilities[value]

    return v
    """
    return 0
