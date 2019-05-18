#!/usr/bin/env python3
from collections import OrderedDict
import csv
from datetime import datetime
import json
import time

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
		self.ohOhSeven = None
		# self.format = None
		self.customProperties = {
			# defining some properties specific to our project here
			'MonoStereo':None,	# set to mono/stereo/surround/unknown for 344/007 use
			'yyyymmdd':None,
			'duration':None,
			'format':"REC", 	# This is the 3-letter MARC format code
			'BLvl':'m', 		# level of bibliographic description
			'Ctry':'cau',		# MARC country code
			'Dates':'\\\\\\\\\\\\\\\\',	# Date1+Date2
			'DtSt':'s',			# Date Status ('s' for single)
			'ELvl':'m',			# Encoding level ('m' for minimal)
			'Form':'o',			# Form of item
			'Lang':'eng',		# Language of material
			'LTxt':'lt',		# 008 audio textual content;
								#   set to 'l' for lecture, 't' for interview
			'Time':'\\\\\\',	# duration in minutes
			'Type':'i',			# 1-letter code for "type of record"
			"NumberOfFiles":""	# number of files in the resource, used in 300
			}
		self.asJSON = {}

	def to_json(self):
		# YEAH ITS A DICT NOT JSON, SHUT UP
		temp = {
			"leader":self.leader,
			"fields": [
				{"007":self.ohOhSeven},
				{"008":self.ohOhEight}
			]
		}

		for field in self.dataFields:
			fieldDict = {
				field.tag:{
					"ind1":field.ind1,
					"ind2":field.ind2,
					"subfields":[]
				}
			}
			for subfield in field.subfields:
				subfield.value = subfield.value.replace('/',r'\/')
				fieldDict[field.tag]["subfields"].append(
					{subfield.subfieldCharacter:subfield.value}
					)
			temp['fields'].append(fieldDict)

		# SORT THE FIELDS BY TAG NUMBER
		temp['fields'] = sorted(temp['fields'], key= lambda t: list(t.keys())[0])

		self.asJSON = temp
		
class Collection:
	'''
	Just a list of Record objects
	'''
	def __init__(self):
		self.records = []

def parse_csv(Record):
	for field,elements in MARCmapper.MARCmapper.items():
		if not elements['status']:
			# i.e., if there are not separate processing instructions
			if Record.fieldedData[field] not in (None,"None",""," "):
				# i.e., if there is actually data in the CSV
				theValue = Record.fieldedData[field]
				marcField = fields.DataField(
					elements['tag'],
					elements['ind1'],
					elements['ind2']
					)
				for subfieldDict in elements['subfields']:
					if 'prefix' in subfieldDict.keys():
						theValue = subfieldDict['prefix']+theValue
					if 'suffix' in subfieldDict.keys():
						theValue = theValue+subfieldDict['suffix']
					for key,value in subfieldDict.items():
						if not key in ('prefix','suffix'):
							if value == 'value':
								sfContent = theValue
							else:
								sfContent = value

							theSF = fields.Subfield(key,sfContent)
							marcField.subfields.append(theSF)
				# ADD THE FIELD TO THE RECORD
				Record.dataFields.append(marcField)

def set_fixed_field(Record):
	'''
	BASED ON THE CUSTOM STUFF SET IN RECORD.customProperties,
	CREATE LDR AND 008 FIELDS.
	ALSO, PARSE AN 007 FROM THE 'FORMAT' PROPERTY AND THE 
	CUSTOM VALUES IN MARCmapper.set_ohOhSeven()
	'''
	ffBytes = fields.ItemBytes(
		format=Record.customProperties['format'],
		BLvl=Record.customProperties['BLvl'],
		Ctry=Record.customProperties['Ctry'],
		Dates=Record.customProperties['Dates'],
		DtSt=Record.customProperties['DtSt'],
		ELvl=Record.customProperties['ELvl'],
		Form=Record.customProperties['Form'],
		Lang=Record.customProperties['Lang'],
		LTxt=Record.customProperties['LTxt'],
		Time=Record.customProperties['Time'],
		Type=Record.customProperties['Type']
		)
	ffBytes.set_008_bytes()
	if ffBytes:
		Record.leader = fields.Leader(ffBytes).data
		Record.ohOhEight = fields.OhOhEight(ffBytes).data

	Record.ohOhSeven = MARCmapper.set_ohOhSeven(Record)

def main():
	collectionDict = dataHandlers.main()

	myCollection = Collection()

	# counter = 0
	for recordUUID,data in collectionDict.items():
		onerecord = Record(data)
		MARCmapper.main(onerecord)
		parse_csv(onerecord)
		set_fixed_field(onerecord)
		onerecord.to_json()

		myCollection.records.append(onerecord.asJSON)
		# counter += 1
		# if counter > 4:
		# 	break

	with open('data/output.json','w') as f:
		json.dump(myCollection.records,f)

if __name__ == "__main__":
	main()