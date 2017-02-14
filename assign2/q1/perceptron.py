'''
Written for Python 3.5.2
This program is an implementation of the Perceptron algorithm.
Tested using a .csv file as input with only numeric attributes.
Output is the values learned and a graph of the separator line.
'''
import numpy as np
import os, sys
import matplotlib.pyplot as pyplot
################################################################################
# read_file(fname)                                                             #
# Input: file name corresponding to file we wish to read                       #
# Output: contents of file if it can be read, otherwise an error code          #
################################################################################
def read_file(fname):
    if os.path.exists(fname):
        # First, check for proper extension
        fext = fname.split(".")[1]
        if fext not in ('txt', 'csv','arff'):
            print("Invalid input file."
                  "Looking for a file of .arff, .csv or .txt format")
            exit(1)
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
            classvals.append(int(line[-1]))
            line = line[:-1]
            while len(line) < 3:
                line += [1]
            tmpline = []
            for item in line:
                try:
                    tmpline.append(float(item))
                except ValueError:
                    tmpline.append(item)
            traindata.append(tmpline)
        traindata = np.matrix(traindata)
        return (traindata, classvals, header)
    # If we hit this the file we're looking for is not in its expected directory
    print("Error: '{}' not found. Input valid data.".format(fname))
    exit(1)
################################################################################
# Input: data                                                                  #
# Output: set of w's corresponding to separator line                           #
################################################################################
def perceptron(traindata, classvals, dataheaders):
    # We want at least a 2D line, so ensure there are at least 3 w values
    w = np.matrix([np.random.rand(len(dataheaders)-1)])
    print("Randomly generated w values:", w)
    # eta can be set to any value such that 0 < eta <= 1
    eta = 0.01
    # t is the number of training loops we conduct. Alter as desired
    for t in range(100):
        i = 0
        for row in traindata:
            sign = row.dot(w.transpose())
            if classvals[i]*row.dot(w.transpose()) <= 0:
                w = w + eta*classvals[i]*row
            i += 1
    return w.tolist()
################################################################################
#                     P R O G R A M    S T A R T S    H E R E                  #
################################################################################
def main():
    if len(sys.argv) != 2:
        print("Not enough arguments. Usage of program: perceptron.py inputfile")
        exit(0)
    print("Attempting to read", sys.argv[1])
    # Get back a tuple containing data & headers in correct order
    traindata = read_file(sys.argv[1])
    sepline = perceptron(traindata[0], traindata[1], traindata[2])[0]

    print("Learned w values:", sepline)
    print("Generating plot using w values to find points on line.")
    graphline = []
    # x1 = -(b+w2x2)/w1
    for i in range(10):
        graphline.append(-(sepline[0]*i+sepline[2])/sepline[1])
    pyplot.plot(graphline)
    pyplot.suptitle("Perceptron line for {}".format(sys.argv[1]))
    pyplot.show()
if __name__ == "__main__":
    main()
