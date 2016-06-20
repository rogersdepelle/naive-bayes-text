# -*- coding: utf-8 -*-

__author__ = "Rogers de Pelle"
__contact__ = "@rogersdepelle"


import copy
import json
import sys
import math
import os
import re
import time
import warnings

from naive_bayes import learn, classify


def standard_deviation(s):
    """
        s: Values list for calculate standard deviation
    """
    avg = sum(s)/float(len(s))
    var = map(lambda x: (x - avg)**2, s)
    return math.sqrt(sum(var)/float(len(var)))


def clean_text(text, option):
    """
        text: String
        option: Filter option to be applied in the text
    """
    text = re.sub('<[^>]*>', '', text)
    text = re.sub('[.,;!?]', ' ', text)
    if option == 2 or option == 4:
        text = re.sub('[^a-zA-Z ]', '', text)
    if option == 3 or option == 4:
        warnings.simplefilter("ignore", UnicodeWarning)
        file = open(os.path.dirname(__file__) + '/stopwords.json', 'r')
        stopwords = json.loads(file.read())
        text = ' '.join([word for word in text.split() if word not in stopwords])
    return text


def get_text(begin, end, positive_path, negative_path, option):
    """
        positive_path: Path of positive files
        negative_path: Path of negatives files
    """

    docs = {'pos':[], 'neg':[]}

    for x in xrange(begin,end+1):
        try:
            file_path = positive_path + str(x) + ".txt"
            file = open(file_path)
            docs['pos'].append(clean_text(file.read(), option))
        except:
            print "Invalid file: " + file_path
            sys.exit(0)
        try:
            file_path = negative_path + str(x) + ".txt"
            file = open(file_path)
            docs['neg'].append(clean_text(file.read(), option))
        except:
            print "Invalid file: " + file_path
            sys.exit(0)

    return docs


def cross_validation(docs, values, k):
    """
        docs: Dict with text lists separate by value
        values: Target values texts
        k: Steps of cross validation
    """

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


def evaluation(confusion_matrix, log, values):
    """
        confusion_matrix: Partial confusion matrices
        log: Recording the results
    """

    i = 0
    matrix = {'true':{}, 'false':{}}

    for value in values:
        matrix['true'][value] = []
        matrix['false'][value] = []

    for m in confusion_matrix:
        i += 1
        log.write("Matrix " + str(i))
        for value in values:
            log.write("\nTrue %s: %5d | False %s: %5d" % (value, m['true'][value], value, m['false'][value]))
            matrix['true'][value].append(m['true'][value])
            matrix['false'][value].append(m['false'][value])
        log.write("\n\n")

    log.write("General Matrix")
    for value in values:
        log.write("\nTrue %s: %5d | False %s: %5d" % (value, sum(matrix['true'][value]), value, sum(matrix['false'][value])))

    log.write("\n\nStandard Deviation")
    for value in values:
        log.write("\nTrue %s: %5.2f | False %s: %5.2f" % (value, standard_deviation(matrix['true'][value]), value, standard_deviation(matrix['false'][value])))

    return matrix


def main():
    start = time.time()
    values = ['pos', 'neg']
    option = -1
    begin = 0
    end = 24999

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

    print "\nNaive Bayes:"
    print "\nChoose the files range (0-24999)"

    while option < begin or option > end:
        try:
            option = int(raw_input('\nBegin: '))
            if option < begin or option > end:
                print "\nInvalid Number!"
        except:
            option = 0
            print "\nInvalid Number!"

    begin = option

    while option <= begin or option > end or option - begin < 10:
        try:
            option = int(raw_input('\nEnd: '))
            if option <= begin or option > end or option - begin < 10:
                print "\nInvalid Number!"
        except:
            option = 0
            print "\nInvalid Numbern!"

    end = option
    option = 0

    print "\n1. Basic classification"
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

    docs = get_text(begin, end, positive_path, negative_path, option)
    confusion_matrix = cross_validation(docs, values, 10)

    log = open('log' + str(option) + '.txt', 'w')
    matrix = evaluation(confusion_matrix, log, values)

    tp = sum(matrix['true']['pos'])
    tn = sum(matrix['true']['neg'])
    fp = sum(matrix['false']['pos'])
    fn = sum(matrix['false']['neg'])
    precision = (tp / float(tp + fp))
    recall = (tp / float(tp + fn))
    f1 = 2 * precision * recall / (precision + recall)

    log.write("\n\nPrecision: %.2f%%" % (precision * 100))
    log.write("\nRecall: %.2f%%" % (recall * 100))
    log.write("\nTrue pos: " + str(tp))
    log.write("\nFalse pos: " + str(fp))
    log.write("\nF1 Score: %.2f%%" % (f1 * 100))
    log.write("\nTime: %.0fs" % (time.time() - start))

    log.close()
    print "\nThe results were saved the log" + str(option) + ".txt\n"


if __name__ == "__main__":
    main()
