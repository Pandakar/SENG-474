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
################################################################################
# update_dictionary(d, words)                                                  #
# INPUT:  a dictionary and the words we want to insert                         #
# OUTPUT: updated dictionary                                                   #
################################################################################
def update_dictionary(d, words):
    keys = d.keys()
    for word in words:
        if word in keys:
            d[word] += 1
        else:
            d[word] = 1
    return d
################################################################################
# read_data(datafile, labelfile)                                               #
# Input: two file names, one for the data and one for the data's class vals    #
# Output: a dictionary for each class with word frequencies                    #
################################################################################
def read_data(datafile, labelfile):
    if os.path.exists(datafile) and os.path.exists(labelfile):
        labels = (open(labelfile, 'r')).readlines()
        data = (open(datafile, 'r')).readlines()
        predictions = {} # for all labels == 1
        sayings = {}     # for all labels == 0
        for i in range(len(data)):
            sentence = data[i].strip('\n').split()
            if int(labels[i]) == 1:
                predictions = update_dictionary(predictions, sentence)
            else:
                sayings = update_dictionary(sayings, sentence)
        return (predictions, sayings)
    else:
        print("Error: one of {} or {} not at correct location.".format(datafile, labelfile))
        exit(0)

def main():
    if len(sys.argv) != 5:
        print("Error: need 4 additional arguments for program. Run program as follows:"
              "python naive_bayes.py traindata trainlabels testdata testlabels")
        exit(0)
    # 1) Read the training data and the training labels
    predictions, sayings = read_data(sys.argv[1], sys.argv[2])
    # 3) Build a learning scheme based on training data & labels
    # 4) Read the testing data
    # 5) Read the testing labels
    # 6) Run against the testing data, return a matrix pertaining to guesses
    # 7) Verify accuracy against testing labels

if __name__ == "__main__":
    main()
