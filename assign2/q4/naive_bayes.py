'''
Written for Python 3.5.2

This program is an implementation of a Naive Bayes classifier for text
classification. This implementation is intended for use on fortune cookie
messages that can be split into two classes:

     - messages that predict what will happen in the future
     - messages that just contain a wise saying

The implementation of Naive Bayes here is a multinomial approach omitting
feature selection. We consider all terms within our training data.
'''
import numpy, matplotlib
import os, sys
from math import log as ln, fabs  # Math library uses base e
################################################################################
# extract_vocabulary(document)                                                 #
# INPUT:  document to train classifier off                                     #
# OUTPUT: dictionary with our desired vocab                                    #
################################################################################
def extract_vocabulary(document):
    vocab = {}
    for sentence in document:
        for word in sentence.strip('\n').split():
            if word in vocab.keys():
                vocab[word] += 1
            else:
                vocab[word] = 1
    return vocab
################################################################################
# count_docs_in_class(document, classes, c)                                    #
# INPUT:  class label associations for docs and class as filter                #
# OUTPUT: number of documents matching class c                                 #
# Since we only care about the number of docs of class c, we can get away with #
# just using the class label list here.                                        #
################################################################################
def count_docs_in_class(classes, c):
    nc = 0
    for i in range(len(classes )):
        if classes[i] == c:
            nc += 1
    return nc
################################################################################
# concatenate_documents_of_class(document, classes, c)                         #
# INPUT:  document to read from, associated class labels, and filter class     #
# OUTPUT: a dictionary pertaining to the text in document associated with      #
#         class c, along with word counts                                      #
################################################################################
def concatenate_documents_of_class(document, classes, c):
    concat = {}
    numterms = 0
    for i in range(len(document)):
        if classes[i] == c:
            sentence = document[i]
            for word in sentence.strip('\n').split():
                numterms += 1
                if word in concat.keys():
                    concat[word] += 1
                else:
                    concat[word] = 1
    return concat, numterms
################################################################################
# train_multinomialNB(labelfile, datafile)                                     #
# INPUT:  classes and document to train on                                     #
# OUTPUT: the vocabulary we're working with, prior (?)                         #
#         and associated conditional probabilities                             #
# Note that for the fortune cookies:                                           #
# class 0 -> wise sayings                                                      #
# class 1 -> predictions                                                       #
################################################################################
def train_multinomialNB(datafile, labelfile):
    document = (open(datafile, 'r')).readlines()
    classes = (open(labelfile, 'r')).readlines()
    vocab = extract_vocabulary(document)
    n = len(document)
    print("Vocabulary extracted, using {} tuples for training.".format(n))
    # strip off newlines to ensure we can pull unique classes
    for i in range(len(classes)):
        classes[i] = classes[i].strip('\n')
    classtypes = list(set(classes))
    prior = {}
    condprob = {}
    for c in classtypes:
        nc = count_docs_in_class(classes, c)
        prior[c] = nc/n
        textc,numterms = concatenate_documents_of_class(document, classes, c)
        vocab_cardinality = len(vocab.keys())
        for term in vocab:
            #print("P({}|{}) =...".format(term, c))
            if term in textc.keys():
                condprob[(term, c)] = (textc[term] + 1)/(numterms+vocab_cardinality)
            else:
                condprob[(term,c)] = 0

    # DEBUG
    #for key in condprob.keys():
    #    print("{} -> {}".format(key, condprob[key]))

    return vocab,prior,condprob
################################################################################
# apply_multinomialNB(C,V,prior,condprob,d)
# INPUT:  Class list, vocab, prior probabilities, conditional probabilites and
#         document we want to classify
# OUTPUT: arg max_(c in C) score[c]
################################################################################
def apply_multinomialNB(C,V,prior,condprob,d):
    w = d.strip().split()
    score = {}
    for c in C:
        score[c] = ln(prior[c])
        for t in w:
            if (t in V.keys() and condprob[(t,c)] > 0):
                score[c] += ln(condprob[(t,c)])
    # since we're dealing with logs of probabilites, flip signs for accurate guesses
    for key in score.keys():
        score[key] = fabs(score[key])
        #print("{}: {}".format(key, score[key]))
    # http://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary#comment19151924_268285
    return max(score.keys(), key=(lambda key: score[key]))
################################################################################
#                     P R O G R A M    S T A R T S    H E R E                  #
################################################################################
def main():
    if len(sys.argv) != 5:
        print("Error: need 4 additional arguments for program."
              "Run program as follows:"
              "python naive_bayes.py traindata trainlabels testdata testlabels")
        exit(0)
    # verify all arguments lead to some OS path
    for arg in range(1,5):
        if not os.path.exists(sys.argv[arg]):
            print("Couldn't find {}. Check input files".format(sys.argv[arg]))
            exit(1)
    # Quick mapping from argvs to additional variables for readability
    traindata = sys.argv[1]
    trainlabel = sys.argv[2]
    testdata = sys.argv[3]
    testlabel = sys.argv[4]
    # Get training data required for guesswork
    vocab, prior, condprob = train_multinomialNB(traindata, trainlabel)
    # Read in test data and test labels associated
    testdata = (open(testdata, 'r')).readlines()
    testlabel = (open(testlabel, 'r')).readlines()
    numright = 0
    for i in range(len(testlabel)):
        testlabel[i] = testlabel[i].strip('\n')
    classtypes = list(set(testlabel))

    for i in range(len(testdata)):
        guess = apply_multinomialNB(classtypes, vocab, prior, condprob, testdata[i])
        #print("For doc {}, guessed {} (ANSWER: {})".format(i, guess, testlabel[i]))
        if guess == testlabel[i]:
            numright += 1

    print("FINAL RESULTS")
    print("Accuracy: {} (from {}/{})".format(numright/len(testlabel), numright, len(testlabel)))
if __name__ == "__main__":
    main()
