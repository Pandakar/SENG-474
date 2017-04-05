

import csv

with open('results.txt', 'r') as run:
    with open('results.csv', 'a') as outfile:
        csvwriter = csv.writer(outfile,delimiter=',')
        lines = run.readlines()
        vocab = [lines[0].split(': ')[1].strip('\n')]
        results = lines[2].split(' | ')
        row = vocab + results
        csvwriter.writerow([int(item) for item in row])
        
            
