'''
Written for Python 3.5.2
This program is an implementation of the Perceptron algorithm.
'''
import numpy as np
import os, sys
from random import random
# http://stackoverflow.com/questions/714063/importing-modules-from-parent-folder
# Read through later and see if this is helpful for reducing redundancy between assignment programs
# Input: file name corresponding to file we wish to read
# Output: contents of file if it can be read, otherwise an error code
# This function handles errors related to invalid data input.
# Current list of possible invalid errors:
#   - inputted file has no way of being data (not .txt, .csv, .arff)
def read_file(fname):
    if os.path.exists(fname):
        # First, check for proper extension
        fext = fname.split(".")[1]
        if fext not in ('txt', 'csv','arff'):
            print("Invalid input file."
                  "Looking for a file of .arff, .csv or .txt format")
            exit(0)
        lines = open(fname, 'r')
        # split header row into attributes and classval
        header = lines.readline().strip('\n').split(',')
        olen = len(header)
        print("Column headers:", header)
        # determine here if we need additional dummy columns to match w's
        # stick filler cols between attrs and classval
        while len(header) < 4:
            header = header[:-1] + ['x'] + header[-1:]
        if olen < len(header):
            print("Adding dummy columns to data to fit as a 2D line.\n"
            "New column headers:", header)
        traindata = []
        classvals = []
        for line in lines:
            line = line.strip('\n').split(',')
            # Dummy data only filled if length not adequate
            classvals.append(line[-1:])
            line = line[:-1]
            while len(line) < 3:
                line += [1]
            traindata.append(line)
        traindata = np.matrix(traindata)
        classvals = np.matrix(classvals)
        print(traindata)
        print(classvals)
        return (traindata, classvals, header)
    # If we hit this the file we're looking for is not in the current directory
    print("Error: not found in cwd. Input valid data.", fname)
    exit(0)

# Input: data
# Output: set of w's corresponding to separator line
def perceptron(traindata, classvals, dataheaders):
    # We want at least a 2D line, so ensure there are at least 3 w values
    w = np.matrix([random() for _ in range(len(dataheaders)-1)])
    print("Randomly generated w values:", w)
    nrows = w.shape[0]
    i = 0
    eta = 0.01
    correctlyClassified = False
    #while not correctlyClassified :
    #    if i
    #h(x, w) = sign(w^Tx) = sign(w dot x)

def main():
    if len(sys.argv) != 2:
        print("Not enough arguments. Usage of program: perceptron.py inputfile")
        exit(0)
    print("Attempting to read", sys.argv[1])
    # Get back a tuple containing data & headers in correct order
    traindata = read_file(sys.argv[1])
    print(traindata[2][-1], "is the class value")
    perceptron(traindata[0], traindata[1], traindata[2])
if __name__ == "__main__":
    main()
