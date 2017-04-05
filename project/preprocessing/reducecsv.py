from hashlib import sha1
import csv
import sys
###############################################################################
# filter_stopwords(text)                                                      #
# INPUT: text to filter stopwords from                                        #
# OUTPUT: text with commonly used 'noisy' terms stripped out                  #
###############################################################################
def filter_stopwords(text):
    newtext = ""
    with open('stopWords.txt', 'r') as stopwords:
        punctuation = ['"', ',', ';', '!', '?', '.', '`']
        noisy_terms = [term.strip() for term in (stopwords.readlines())]
        for term in text.split(' '):
            term = (((term.replace('\n', '')).replace('\t', '')).replace('\r', '')).lower()
            for item in punctuation:
                term = term.replace(item, ' ')

            if term not in noisy_terms:
                newtext += term + ' '
    return(newtext)

###############################################################################
#
###############################################################################
with open('smallerfake.csv', 'r') as csvfile:
    csvread = csv.reader(csvfile, delimiter=',')
    with open('reducednews.csv', 'wb') as outfile:
        csvwrite = csv.writer(outfile, delimiter=',')
        hashlist = []
        origarticles = 0
        lenorig = 0
        for row in csvread:
            row = [item.decode('utf-8') for item in row]
            # Row order: uuid, title, text, domain, class
            if row[0] != "uuid":
                row[0] = sha1(row[1].encode('utf-8')+row[3].encode('utf-8')).hexdigest()
                if row[0] in hashlist:
                    continue
                origarticles += 1
                lenorig += len(row[2])
                hashlist.append(row[0])
                text = [filter_stopwords(row[2])]
                row = row[0:2] + text + row[3:]
            csvwrite.writerow([item.encode('utf-8') for item in row])
        print("# articles: {}\nTotal len: {}\nAverage len per article: {}".format(origarticles, lenorig, (lenorig/origarticles)))
