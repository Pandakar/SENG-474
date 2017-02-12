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
import numpy, matplotlib, pandas
import os
def linear_regression():
    x = numpy.matrix([[1,1],[1,2]])
    y = numpy.matrix([[1.5], [2]])
    w = numpy.array([[2], [2]])
    kappa = 0.1
    n = len(y)
    # Need to transform the given Octave equation into Python equivalent
    # The '  symbol refers to transpose
    # The .* symbol refers to elementwise multiplication
    #     x*w produces a dot product?
    for t in range(1,11):
        # w = w + kappa*(1/n)*sum((y-x*w).*x)'
        # -> w = w + kappa*(1/n)*
        print(t)
# Input: file name corresponding to file we wish to read
# Output: contents of file if it can be read, otherwise an error code
def read_file(fname):
    # if fname exists in os:
    #     try:
    #         read(fname)
    #         return file_contents
    #     except file_errors:
    #         return corresponding error code
    pass

def scale_attributes():
    pass

def compute_error():
    pass

def plot_error():
    pass

def error_learning():
    pass
def main():
    print("Hello, world!")

if __name__ == "__main__":
    main()
