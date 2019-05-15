#!/usr/bin/env python3
import csv
import os
import sys
import uuid 

def get_data_csv():
	# there should only be one at a time?
	here = os.path.dirname(os.path.abspath(__file__))
	dataDir = os.path.join(here,'data')
	dataPath = [
		x.path for x in os.scandir(dataDir) if x.name.endswith(".csv")
		][0]

	return dataPath

def rows_to_json(dataPath):
	with open(dataPath,'r') as f:
		reader = csv.reader(f)
		headers = next(reader)
		data = [row for row in reader]

	collectionJSON = {}
	print(headers)
	# sys.exit()

	for record in data:
		# print(record)
		recordUUID = str(uuid.uuid4())
		collectionJSON[recordUUID] = {}
		for column in headers:
			collectionJSON[recordUUID][column] = record[headers.index(column)]

	return collectionJSON

def main():
	dataPath = get_data_csv()
	collectionJSON = rows_to_json(dataPath)

	print(collectionJSON)
	return collectionJSON

if __name__ == "__main__":
	main()
