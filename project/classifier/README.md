# Naive Bayes

This java program is an implementation of the Naive Bayes multinomial algorithm.
Its primary purpose is to run through a CSV file containing news article text.

To compile this program on Windows:
`javac -cp ".;opencsv-3.9.jar;commons-lang3-3.5.jar" naiveBayes.java`

To compile this program on Linux:
`javac -cp "opencsv-3.9.jar:commons-lang3-3.5.jar" naiveBayes.java`

To run this program through Windows cmd:
`java -cp ".;opencsv-3.9.jar;commons-lang3-3.5.jar" naiveBayes input.csv`

To run in Linux:
`java -cp "opencsv-3.9.jar:commons-lang3-3.5.jar" naiveBayes /path/to/input.csv`

Input CSVs should contain a header row with the following:
uuid,title,text,domain,class

Attributes in the CSV are used as follows.

| uuid | title | text | domain | class |
|:----:|:-----:|:----:|:------:|:-----:|
| unique identifier | unused | used for classification | unused | used for verifying guesses |

A sample CSV can be found in ../sampledata. 
