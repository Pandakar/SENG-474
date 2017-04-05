# Script used to automatically cycle through all articles in defined csvs
# Testing on Ubuntu systems
datadir='../sampledata/'
for f in ../sampledata/*.csv; do
  echo $f
  time java -cp ".:opencsv-3.9.jar:commons-lang3-3.5.jar" naiveBayes $f > results.txt
  python resultwriter.py
done
