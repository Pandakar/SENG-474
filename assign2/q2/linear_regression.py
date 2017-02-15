'''
Written for Python 3.5.2
This program is an extension of the linear regression algorithm featured in this course.
This extension adds the following capabiltiies:
- Reading data from files
- Scaling attributes
- Computing error at each iteration and saving error values in a vector
- Plotting error vector as a curve for output
- Find a good learning rate based on error curve
'''
import numpy as np, matplotlib, pandas
import os, sys
import random
################################################################################
# linear_regression()
################################################################################
def linear_regression(traindata, classvals):
    w = np.matrix([random.sample(range(-10,10), len(traindata.transpose()))])
    print("Initial w vector:", w)
    kappa = 0.9
    n = len(traindata)
    # Learn the proper weights for w after initializing
    # Run for 100 loops or until w doesn't change, whichever comes first
    for t in range(100):
        i = 0
        initw = w
        for x in traindata:
            w = w + kappa/n*(np.sum(np.multiply((classvals[i]-x.dot(w.transpose())), x).transpose()))
            i += 1
        if ((w == initw[0]) - 0).all():
            break
    # DEBUG - printing /99 since range(100) = [0, 99]
    print("w vector settled to {} after {}/99 loops".format(w, t))
    return w
################################################################################
# read_file(fname)
# Input: file name corresponding to file we wish to read
# Output: contents of file if it can be read, otherwise an error code
################################################################################
def read_file(fname):
    if os.path.exists(fname):
        f = open(fname)
        # Don't really care about labels for now
        lines = f.readline()
        lines = f.readlines()
        traindata = np.matrix(list(map(lambda l: list(map(float, l.split(',')[:-1])), lines)))
        # Repeat operation but to grab all classvals in an ordered list
        classvals = list(map(lambda l: int(l.strip().split(',')[-1]), lines))
        return (traindata, classvals)
################################################################################
# scale_attributes
################################################################################
def scale_attributes():
    pass
################################################################################
# compute_error
################################################################################
def compute_error():
    pass
################################################################################
# plot_error()
################################################################################
def plot_error():
    pass
################################################################################
# error_learning()
################################################################################
def error_learning():
    pass
################################################################################
#                   P R O G R A M    S T A R T S    H E R E                    #
################################################################################
def main():
    if len(sys.argv) < 2:
        print("Error: program incorrectly invoked."
              "Usage of program: 'python linear_regression.py $inputfile'")
        exit(0)
    fdata = read_file(sys.argv[1])
    linear_regression(fdata[0], fdata[1])
if __name__ == "__main__":
    main()
