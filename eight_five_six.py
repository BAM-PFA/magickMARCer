'''
stupid little script to add archive.org urls to data input csv

'''

import csv

def get_urls(urlCSV):
	with open(urlCSV) as urlFile:
		reader = csv.DictReader(urlFile)
		id_to_url = {}
		for row in reader:
			id_to_url[row['item id']] = "https://archive.org/details/{}".format(row['ia id'])

	return id_to_url

def combinator(inputCSV,id_to_url):
	with open(inputCSV) as inFile, open('data-w-856.csv','a') as outFile:
		reader = csv.DictReader(inFile)
		result = csv.DictWriter(outFile, fieldnames=reader.fieldnames + ['url'])
		result.writeheader()
		for row in reader:
			row['url'] = id_to_url.get(row['itemNumber'], '')
			result.writerow(row)

def main():
	inputCSV = input("Give me a file with the existing data: ").rstrip()
	urlCSV = input("Give me a file that includes IA ids with matching item ids: ").rstrip()

	id_to_url = get_urls(urlCSV)
	combinator(inputCSV,id_to_url)

if __name__ == "__main__":
	main()

