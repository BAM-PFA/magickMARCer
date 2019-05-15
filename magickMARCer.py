#!/usr/bin/env python3
import csv
from datetime import datetime
import json
import time
import uuid

import fields
import handlers
from MARCmapper import MARCmapper

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

	def parse_speaker_names(self):
		namesLNFN = self.fieldedData['lnfn'].split('|')
		if namesLNFN != ['']:
			for name in namesLNFN:
				addedEntry = fields.DataField('700','1','',)
				for x in [
					fields.Subfield('a',name),
					fields.Subfield('e','speaker')
					]:
					addedEntry.subfields.append(x)
				self.dataFields.append(addedEntry)

	def parse_film_title_subjects(self):
		titles = self.fieldedData['FilmTitles'].split('|')
		if titles != ['']:
			for title in titles:
				subj = fields.DataField('630','','4')
				subj.subfields.append(
					fields.Subfield('a',title+" (Motion Picture)")
					)
				self.dataFields.append(subj)

	def parse_recording_date(self):
		date = self.fieldedData['recordingDate']
		try:
			date = datetime.strptime(date,'%a %b %d %H:%M:%S PST %Y')
			yyyymmdd = datetime.strftime(date,'%Y%m%d')
		except:
			yyyymmdd = date
		self.yyyymmdd = yyyymmdd
		if len(self.yyyymmdd) == 8:
			recDate = fields.DataField('033','0','0')
			for x in [
				fields.Subfield('a',self.yyyymmdd),
				fields.Subfield('b','4360'),
				fields.Subfield('c','B5')
				]:
				recDate.subfields.append(x)
			self.dataFields.append(recDate)

	def add_collection_defaults(self):
		#$as$bz$du$eu$fn$gn$hn$in$jn$kn$ln$me$nz
		ohOhSeven = fields.DataField('007','','')
		for x in [
			fields.Subfield('a','s'),
			fields.Subfield('b','z'),
			fields.Subfield('d','u'),
			fields.Subfield('e','u'),
			fields.Subfield('f','n'),
			fields.Subfield('g','n'),
			fields.Subfield('h','n'),
			fields.Subfield('i','n'),
			fields.Subfield('j','n'),
			fields.Subfield('k','n'),
			fields.Subfield('l','n'),
			fields.Subfield('m','e'),
			fields.Subfield('n','z')
			]:
			ohOhSeven.subfields.append(x)

		self.dataFields.append(ohOhSeven)

def main():
	collectionJSON = handlers.main()

	# counter = 0
	# while counter < 3:
	# 	for x in collectionJSON:
	# 		print(x)

	for recordUUID,data in collectionJSON.items():
		onerecord = Record(data)
		onerecord.parse_speaker_names()
		print(onerecord.dataFields)

if __name__ == "__main__":
	main()