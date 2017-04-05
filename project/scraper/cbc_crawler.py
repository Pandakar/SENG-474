'''
cbc_crawler.py
Written for Python 2.7.9
To run on CLI:
python cbc_crawler.py

Program depends on a list of RSS feeds.
It reads each RSS feed as an XML page, then extracts metadata for each entry.
After extracting metadata, it visits the news article in question
and extracts its text.

Currently this program only extracts text nicely from CBC articles but
it could be repurposed to handle other pages too.
'''
import requests
import xml.etree.ElementTree as ET
import BeautifulSoup
import time, datetime
from hashlib import sha1
import csv
# constants, default settings
default_publish = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%SZ')
###############################################################################
#  Method for building request handler.                                       #
#  We fake out the headers so servers think we're a web browser               #
#  and not a crawler                                                          #
###############################################################################
def req_handler():
    reqhand = requests.Session()
    reqhand.headers = {'Connection':'keep-alive',
                       'Cache-Control':'max-age=0',
                       'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                       'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                       'Accept-Encoding':'gzip, deflate, sdch',
                       'Accept-Language':'en-US,en;q=0.8',}
    return reqhand
###############################################################################
# filter_stopwords(text)                                                      #
# INPUT: text to filter stopwords from                                        #
# OUTPUT: text with commonly used 'noisy' terms stripped out                  #
# This procedure also removes any extraneous newlines and punctuation at      #
# either end of a term. It leaves punctuation in the middle of a term.        #
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
# fetch_input_sites                                                           #
# Since we want to grab from several sites, it makes little sense to hardcode #
# in program. Fetch the sites we want from a config file of our choice.       #
# Currently we want sites for RSS feeds to scrape from.                       #
###############################################################################
def fetch_input_sites():
    sites_to_read = []
    with open('sites_to_read.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            sites_to_read.append(line.strip())
    return sites_to_read
###############################################################################
#                  P R O G R A M    S T A R T S    H E R E                    #
###############################################################################
sites_to_read = fetch_input_sites()
handler = req_handler()
articles = [("uuid","author","published","title","text","crawled","domain","URL")]
otherarticles = [("uuid","author","published","title","text","crawled","domain","URL")]
hashes = []
# Doing two things with this:
# 1) reading old hashes so we don't refetch old articles -- reduces work
# 2) since p2.7 is dumb, we have to open file in 'wb' mode to avoid newlines
#    which clobbers old file. Fetch old results, and for each article apply
#    filters for reducedarticles file
with open('newsarticles.csv', 'r') as csvfile:
    oldresults = csv.reader(csvfile, delimiter=',')
    for row in oldresults:
        # skip over header row
        if row[0] == "uuid":
            continue
        hashes.append(row[0])
        text = [row[4]]
        rtext = [filter_stopwords(row[4].decode('utf-8'))]
        row = row[0:4] + text + row[5:]
        row = [item.decode('utf-8') for item in row]
        articles.append(row)
        reducedrow = row[0:4] + rtext + row[5:]
        otherarticles.append(reducedrow)

extra_articles = 0
for site in sites_to_read:
    xmlpage = handler.get(site)
    xmlpage = ET.fromstring(xmlpage.content)
    print(site)
    new_articles = 0
    for child in xmlpage.iter('item'):
        link = child.find('link').text
        title = child.find('title').text
        author = child.find('author').text
        uuid = sha1((title+link).encode('utf-8')).hexdigest()
		# If we already recorded the article, just skip over requesting
        if uuid in hashes:
            continue
        # If we couldn't get the article, move to the next one
        article_resp = handler.get(link)
        if article_resp.status_code != 200:
            continue
        article = article_resp.content
        soup = BeautifulSoup.BeautifulSoup(article)
        arttext = soup.find("div", {"class": "story-content"})
        undesirables = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                        'script', 'blockquote', 'ul', 'ol', 'span',
                        'strong', 'em', 'hr',
		                'a', 'p, {"class":"figure-caption"}', 'div']
		# The above list is all the crap we don't want. Filter it out one-by-one
        for tag in undesirables:
		    [tag.extract() for tag in soup.findAll(tag)]
        # After our filtering, if we have nothing left no point in adding an article
        if arttext is None:
            continue

        arttext = arttext.extract()
        arttext = (((str(arttext)[28:-7]).replace("<p>", "")).replace("</p>", "")).strip().decode('utf-8')
        arttext = arttext.replace("&nbsp;", " ")
		# Now that we've filtered down article to what should be only text, strip out stop words
        reduced_text = filter_stopwords(arttext)
        newtup = (uuid, author, default_publish, title, arttext, default_publish, 'www.cbc.ca', link)
        extra_tup = (uuid, author, default_publish, title, reduced_text, default_publish, 'www.cbc.ca', link)
        articles.append(newtup)
        otherarticles.append(extra_tup)
        new_articles += 1
    extra_articles += new_articles
    print("Number of new articles on this pass: {}\n".format(new_articles))

print("Adding {} rows to newsarticles.csv\n".format(len(articles)))
with open('newsarticles.csv', 'wb') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    for article in articles:
        csvwriter.writerow([s.encode('utf-8') for s in article])

print("Adding {} rows to newsarticles.csv\n".format(len(otherarticles)))
with open('reducedarticles.csv', 'wb') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    for article in otherarticles:
        csvwriter.writerow([s.encode('utf-8') for s in article])
