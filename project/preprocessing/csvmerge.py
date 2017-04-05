import csv
with open("allarticles.csv","wb") as fout:
	# first file:
	csvwriter = csv.writer(fout, delimiter=",")
	hashlist = []
	with open("realfinal.csv", 'r') as real:
		csvread = csv.reader(real, delimiter=",")
		for row in csvread:
			if row[0] == "uuid":
				pass
			if row[0] in hashlist:
				continue
			hashlist.append(row[0])
			row = [item.decode('utf-8') for item in row]
			csvwriter.writerow([item.encode('utf-8') for item in row[0:5]])
		pass

	with open("reducedfinal.csv", 'r') as fake:
		csvread = csv.reader(fake, delimiter=",")
		for row in csvread:
			if row[0] == "uuid" or row[0] in hashlist:
				continue
			hashlist.append(row[0])
			row = [item.decode('utf-8') for item in row]
			csvwriter.writerow([item.encode('utf-8') for item in row[0:5]])
