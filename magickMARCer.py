#!/usr/bin/env python3
import argparse
import ast
# from collections import OrderedDict
import configparser
import csv
from datetime import datetime
import json
import os
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
		fieldedData,
		customProperties=None
		):
		self.fieldedData = fieldedData
		self.customProperties = customProperties

		self.dataFields = []

		self.leader = None
		self.ohOhSix = None
		self.ohOhEight = None
		self.ohOhSeven = None

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
		if not elements['instructions']:
			# i.e., if there are not separate processing instructions
			if Record.fieldedData[field] not in (None,"None",""," "):
				# i.e., if there is actually data in the CSV
				theValue = Record.fieldedData[field]
				marcField = fields.DataField(
					elements['tag'],
					elements['ind1'],
					elements['ind2']
					)
				# PARSE OUT ALL THE SUBFIELDS
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

def read_config():
	scriptDirectory = os.path.dirname(os.path.abspath(__file__))
	configPath = os.path.join(scriptDirectory,'config.ini')
	config = configparser.SafeConfigParser()
	config.read(configPath)

	return config

def set_args():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'-d','--dataPath',
		help='path path to data CSV file',
		required=True
		)
	# parser.add_argument(
	# 	'-r','--recordType',
	# 	help=(
	# 		'3-letter MARC code for record type (BKS,REC,VIS,etc.)'
	# 		'This code should apply to all the records in the CSV...'
	# 		),
	# 	required=True
	# 	)
	parser.add_argument(
		'-c','--configProperties',
		help=(
			'This should correspond the name of a dict defined in config.ini '
			'which will define properties used in fixed field, 007, 300, etc.'
			),
		required=True
		)
	parser.add_argument(
		'-o','--outputPath',
		help=(
			'Path to directory where you want the output JSON file to live. '
			'Default is in the ./data directory under this folder.'
			),
		default='./data/'
		required=True
		)

	return parser.parse_args()

def main():
	args = set_args()
	dataPath = args.dataPath
	# recordType = args.recordType
	print(dataPath)
	configProperties = args.configProperties


	config = read_config()
	customProperties = config['customProperties'][configProperties]
	customProperties = ast.literal_eval(customProperties)

	collectionDict = dataHandlers.main(dataPath)

	myCollection = Collection()

	# counter = 0
	for recordUUID,data in collectionDict.items():
		onerecord = Record(data,customProperties)
		MARCmapper.main(onerecord)
		parse_csv(onerecord)
		set_fixed_field(onerecord)
		onerecord.to_json()
		# print(onerecord.customProperties['yyyymmdd'])

		myCollection.records.append(onerecord.asJSON)
		# counter += 1
		# if counter > 4:
		# 	break

	with open('data/output.json','w') as f:
		json.dump(myCollection.records,f)

if __name__ == "__main__":
	main()