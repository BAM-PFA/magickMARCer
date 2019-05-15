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

		self.dataFields = []
		self.leader = None
		self.ohOhSix = None
		self.ohOhEight = None
		self.customProperties = {
			# defining some properties specific to our project here
			'MonoStereo':None,
			'yyyymmdd':None,
			'duration':None
		}
		self.asDict = {}

	def set_fixed_field(self):
		itemBytes = fields.itemBytes(stuff)
		self.leader = fields.Leader(itemBytes)
		self.ohOhSix = fields.ohOhSix(itemBytes)
		self.ohOhEight = fields.ohOhEight(itemBytes)

	def to_json(self):
		temp = {
			"leader":self.leader,
			"fields": [
				{"001":""},
				{"005":""}
			]
		}
		for field in self.dataFields:
			fieldDict = {
				field.tag:{
					"subfields":[],
					"indicator1":field.indicator1,
					"indicator2":field.indicator2
				}
			}
			for subfield in field.subfields:
				fieldDict[field.tag]["subfields"].append(
					{subfield.subfieldCharacter:subfield.value}
					)
			temp['fields'].append(fieldDict)
		self.asDict = temp
		
class Collection:
	'''
	Just a list of Record objects
	'''
	def __init__(self):
		self.records = {}

def main():
	collectionJSON = dataHandlers.main()

	myCollection = Collection()

	for recordUUID,data in collectionJSON.items():
		onerecord = Record(data)
		MARCmapper.main(onerecord)
		onerecord.to_json()

		myCollection.records[recordUUID] = onerecord.asDict

	# for k,v in myCollection.records.items():
	# 	print(v.dataFields)
	print(myCollection.records)

if __name__ == "__main__":
	main()