#!/usr/bin/env python3
import csv
from datetime import datetime
import json
import time
import uuid

import fields
import dataHandlers
import MARCmapper

class Record:
	'''
	Take in a dict of fieldedData and parse out a MARC record in JSON....
	fieldedData looks like { UUID : {field:value,field:value,etc.} }
	'''
	def __init__(
		self,
		fieldedData
		):
		self.fieldedData = fieldedData
		for k,v in self.fieldedData.items():
			self.recordUUID = k

		self.dataFields = []
		self.customProperties = {
			# defining some properties specific to our project here
			'MonoStereo':None,
			'yyyymmdd':None,
			'duration':None
		}
		
class Collection:
	'''
	Just a list of Record objects
	'''
	def __init__(self):
		self.records = []

def main():
	collectionJSON = dataHandlers.main()

	myCollection = Collection()

	for recordUUID,data in collectionJSON.items():
		onerecord = Record(data)
		MARCmapper.main(onerecord)

		myCollection.records.append(onerecord)

	for arecord in myCollection.records:
		print(arecord.dataFields)

if __name__ == "__main__":
	main()