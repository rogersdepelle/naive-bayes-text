# -*- coding: utf-8 -*-

import sys
import os
import re
import copy
import math
import time

from naive_bayes import learn, classify


def standard_deviation(s):
    avg = sum(s)/float(len(s))
    var = map(lambda x: (x - avg)**2, s)
    return math.sqrt(sum(var)/float(len(var)))


def get_text(positive_path, negative_path, option):

    docs = {'pos':[], 'neg':[]}

    for x in xrange(0,50):
        try:
            pos_file_path = positive_path + str(x) + ".txt"
            pos_file = open(pos_file_path)
            #romoving tags
            docs['pos'].append(re.sub('<[^>]*>', '', pos_file.read()))
        except:
            print "Invalid file: " + pos_file_path
            sys.exit(0)
        try:
            neg_file_path = negative_path + str(x) + ".txt"
            neg_file = open(neg_file_path)
            #romoving tags
            docs['neg'].append(re.sub('<[^>]*>', '', neg_file.read()))
        except:
            print "Invalid file: " + neg_file_path
            sys.exit(0)

    """
    # [{(-_+.^:,;)Σ}]
    # [{(-_+.^:,;/!#$%&?@*^*~¨ )Σ}]
    if option = 1 or option = 3:
        remove special caracteres
    if option = 2 or option = 3:
        remove stopwords
    """

    return docs


def cross_validation(docs, values, k):
    
    group_size = {}
    confusion_matrix = []
    m = {'true':{}, 'false':{}}

    for value in values:
        group_size[value] = len(docs[value])/k
        m['true'][value] = 0
        m['false'][value] = 0

    for i in xrange(0,k):
        training = copy.deepcopy(docs)
        confusion_matrix.insert(i, copy.deepcopy(m))
        for value in values:
            begin = i * group_size[value]
            end = (i + 1) * group_size[value]
            test = training[value][begin:end]
            del training[value][begin:end]
            probabilities, vocabulary = learn(training, values)
            for doc in test:
                prob_value = classify(doc, probabilities, vocabulary, values)
                if value == prob_value:
                    confusion_matrix[i]['true'][value] += 1
                else:
                    confusion_matrix[i]['false'][prob_value] += 1

    return confusion_matrix


def evaluation(confusion_matrix, values):

    i = 0
    matrix = {'true':{}, 'false':{}}

    for value in values:
        matrix['true'][value] = []
        matrix['false'][value] = []

    for m in confusion_matrix:
        i += 1
        print "\nMatrix " + str(i)
        for value in values:
            print "True %s: %5d | False %s: %5d" % (value, m['true'][value], value, m['false'][value])
            matrix['true'][value].append(m['true'][value])
            matrix['false'][value].append(m['false'][value])

    print "\nGeneral Matrix"
    for value in values:
        print "True %s: %5d | False %s: %5d" % (value, sum(matrix['true'][value]), value, sum(matrix['false'][value]))

    print "\nDesvio Padrao"
    for value in values:
        print "True %s: %5.2f | False %s: %5.2f" % (value, standard_deviation(matrix['true'][value]), value, standard_deviation(matrix['false'][value]))

    return matrix

def main():
    start = time.time()
    values = ['pos', 'neg']
    option = 0
    
    if len(sys.argv) >= 3:
        if os.path.exists(sys.argv[1]) and os.path.exists(sys.argv[2]):
            positive_path = sys.argv[1]
            negative_path = sys.argv[2]
        else:
            print "\nInvalid paths!"
            sys.exit(0)    
    else:
        print "\nInsert folders path.\n"
        sys.exit(0)

    print "\nNaive Bayes:\n"
    print "1. Basic classification"
    print "2. Classification removing special characters"
    print "3. Classification removing stopwords"
    print "4. Classification removing special characters and stopwords"

    while option < 1 or option > 4:
        try:
            option = int(raw_input('\nChose a option: '))
            if option < 1 or option > 4:
                print "\nInvalid option!"    
        except:
            option = 0
            print "\nInvalid option!"

    docs = get_text(positive_path, negative_path, option)
    confusion_matrix = cross_validation(docs, values, 10)
    matrix = evaluation(confusion_matrix, values)

    tp = sum(matrix['true']['pos'])
    tn = sum(matrix['true']['neg'])
    fp = sum(matrix['false']['pos'])
    fn = sum(matrix['false']['neg'])
    precision = (tp / float(tp + fp))
    recall = (tp / float(tp + fn))
    f1 = 2 * precision * recall / (precision + recall)

    print "\nPrecision: %.2f%%" % (precision * 100)
    print "Recall: %.2f%%" % (recall * 100)
    print "True pos: " + str(tp)
    print "False pos: " + str(fp)
    print "F1 Score: %.2f%%" % (f1 * 100)
    print "Time: %.0fs" % (time.time() - start)


if __name__ == "__main__":
    main()