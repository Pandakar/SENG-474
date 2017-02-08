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

def main():
    print("Hello, world!")

if __name__ == "__main__":
    main()
