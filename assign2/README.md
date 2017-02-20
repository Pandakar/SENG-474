#README for a2

This repository contains components for completion of the second assignment in SENG 474 at the University of Victoria.

Four components for this assignment:

| Q# | Corresponding File      |
|----|:------------------------|
| q1 | perceptron.py           |
| q2 | linear_regression.py    | 
| q3 | logistic_regression.pdf |
| q4 | naive_bayes.py          |

All Python files were written for *Python 3.5.2* and tested in Windows environments.

These files require the following libraries to be added:

- numpy
- matplotlib
- pandas

The three above libraries can be fetched using pip.

Details on running each file will be added as these programs are completed.

## perceptron.py

This program takes in a single input parameter: the file from which we are learning. A sample file, `bankruptcy.csv`, is provided. To run perceptron.py:

`python perceptron.py $inputfile`

After reading the contents of the input file, the perceptron algorithm will be applied to the input data. The list of corresponding w values is generated, from which the program derives a list of points to plot to the user's screen. 

## linear_regression.py

NOTE: This is a partial implementation of linear regression. Not all components were able to be finished on time for the assignment deadline.

This program takes in a single input parameter: the file to learn from. A sample file, `regdata.csv` is provided. To run linear_regression.py:

`python linear_regression.py $inputfile`

This program takes in the input data, scales it as required and then applies the linear regression algorithm to continually learn our w line. Currently this program also records the error computed at each iteration and provides a graph of it after computation.

## naive_bayes.py

This program requires four input parameters:

- a document or set of documents to train from
- a list of labels corresponding to classifications for the training documents
- a document or set of documents we wish to test this program against
- a list of labels corresponding to classifications for the test documents

When run on the command line, naive_bayes.py should be run as follows:

`python naive_bayes.py $traindata $trainlabels $testdata $testlabels`

Sample input is located in q4/data. 
