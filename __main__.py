# -*- coding: utf-8 -*-

import sys
import os
import re
import copy


def get_text(positive_path, negative_path, option):

    docs = {'pos':[], 'neg':[]}

    #28,24028
    for x in xrange(20000,20020):
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

    for value in values:
        group_size[value] = len(docs[value])/k

    for i in xrange(0,k):
        training = copy.deepcopy(docs)
        test = {}
        for value in values:    
            begin = i * group_size[value]
            end = (i + 1) * group_size[value]
            test[value] = training[value][begin:end]
            del training[value][begin:end]
    learn_naive_bayes_text(training, values)
        #classify_naive_bayes_text()


def main():
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
    cross_validation(docs, values, 10)


if __name__ == "__main__":
    main()