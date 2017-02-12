'''
Written for Python 3.5.2

This program is an implementation of the Perceptron algorithm.
'''
import numpy, matplotlib, pandas
# http://stackoverflow.com/questions/714063/importing-modules-from-parent-folder
# Read through later and see if this is helpful for reducing redundancy between assignment programs
import os, sys
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
        for line in lines:
            print(line)
        return lines
    # If we hit this the file we're looking for is not in the current directory
    print("Error: not found in cwd. Input valid data.", fname)
    exit(0)

def perceptron():
    pass

def main():
    print("Hello, world!")
    if len(sys.argv) != 2:
        print("Not enough arguments. Usage of program: perceptron.py inputfile")
        exit(0)
    print("Attempting to read", sys.argv[1])
    read_file(sys.argv[1])
if __name__ == "__main__":
    main()
