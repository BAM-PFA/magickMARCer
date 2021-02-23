#!/usr/bin/env python3
import ast
from datetime import datetime
import fields

'''
This file has stuff that is used to map data that is specific to our
particular instance. So:
* MARCmapper is a dict that maps the data coming
  in from our source CSV.
* add_collection_defaults() adds fields to each record that will be consistent
  across this entire collection
* Then there's a set of functions designed to add fields that parse out
  some of our specific data, namely:
  * speaker names (that go to 245 and 700)
  * film titles as subjects (that go to 630)
  * date of recording

Some of that specific data is added to properties of the `Record` class in a
`customProperties` dict.
Maybe this could be set in a config file if this were to be more broadly applicable?
'''

#MARCmapper_TVTV
MARCmapper = {
	"year":{
		"tag":None,
		"instructions":"rawdate",
		"subfields":[],
		"ind1":"\\",
		"ind2":"\\"
	},
	"summary":{
		"tag":"520",
		"instructions":None,
		"subfields":[
			{
				"a":"value"
			}
		],
		"ind1":"\\",
		"ind2":"\\"
	},
	"duration":{
		"tag":"500",
		"instructions":None,
		"subfields":[
			{
				"a":"value",
				"prefix":"Running time: "
			}
		],
		"ind1":"\\",
		"ind2":"\\"
	},
	"note1":{
		"tag":"500",
		"instructions":None,
		"subfields":[
			{
				"a":"value"
			}
		],
		"ind1":"\\",
		"ind2":"\\"
	},
	"DigitizationNotes":{
		"tag":"500",
		"instructions":None,
		"subfields":[
			{
				"a":"value"
			}
		],
		"ind1":"\\",
		"ind2":"\\"
	},
	"title":{
		"tag":"245",
		"instructions":None,
		"subfields":[
			{
				"a":"value",
				"b":" [unedited footage] /",
				"c":"Top Value Television (Production company)"
			}
		],
		"ind1":"0",
		"ind2":"0"
	},
	"itemNumber":{
		"tag":"035",
		"instructions":None,
		"subfields":[
			{
				"a":"value",
				"prefix":"cbpf_"
			}
		],
		"ind1":"\\",
		"ind2":"\\"
	},
	"genreForm":{
		"tag":"655",
		"instructions":None,
		"subfields":[
			{
				"a":"value",
				"2":"lcgft"
			}
		],
		"ind1":"\\",
		"ind2":"0"
	},
	"recordingEventDescription":{
		"tag":"520",
		"instructions":None,
		"subfields":[
			{
				"a":"value",
				"prefix":"Description of the event: "
			}
		],
		"ind1":"8",
		"ind2":"\\"
	},
	"recordingEventRecordingNotes":{
		"tag":"500",
		"instructions":None,
		"subfields":[
			{
				"a":"value",
				"prefix":"Notes about the original analog recording: "
			}
		],
		"ind1":"\\",
		"ind2":"\\"
	},
	"recordingEventTitle":{
		"tag":"500",
		"instructions":None,
		"subfields":[
			{
				"a":"value",
				"prefix":"Title of event: "
			}
		],
		"ind1":"\\",
		"ind2":"\\"
	},
	"recordingLocation":{
		"tag":"500",
		"instructions":None,
		"subfields":[
			{
				"a":"value",
				"prefix":"Location of recording: "
			}
		],
		"ind1":"\\",
		"ind2":"\\"
	},
	"recordingPermissions":{
		"tag":"540",
		"instructions":None,
		"subfields":[
			{
				"a":"value"
			},
			{
				"c":"Speaker release form."
			}
		],
		"ind1":"\\",
		"ind2":"\\"
	},
	"accessionNumber":{
		"tag":"500",
		"instructions":None,
		"subfields":[
			{
				"a":"value",
				"prefix":"Original videotape accession number: "
			}
		],
		"ind1":"\\",
		"ind2":"\\"
	},
	"duration":{
		"tag":"306",
		"instructions":"rawduration",
		"subfields":[],
		"ind1":"\\",
		"ind2":"\\"
	},
	"url":{
		"tag":"856",
		"instructions":None,
		"subfields":[
			{
				"z":"View item on Internet Archive"
			},
			{
				"u":"value"
			}
		],
		"ind1":"4",
		"ind2":"0"
	},
	"subj1":{
		"tag":"650",
		"instructions":None,
		"subfields":[
			{
				"a":"value"
			}
		],
		"ind1":"\\",
		"ind2":"0"
	}
}

# MARCmapper_CLIR = {
# 	"recordingDate":{
# 		"tag":None,
# 		"instructions":"rawdate",
# 		"subfields":[],
# 		"ind1":"\\",
# 		"ind2":"\\"
# 	},
# 	"DigitizationNotes":{
# 		"tag":"500",
# 		"instructions":None,
# 		"subfields":[
# 			{
# 				"a":"value"
# 			}
# 		],
# 		"ind1":"\\",
# 		"ind2":"\\"
# 	},
# 	"recordingEventDescription":{
# 		"tag":"520",
# 		"instructions":None,
# 		"subfields":[
# 			{
# 				"a":"value",
# 				"prefix":"Description of the event: "
# 			}
# 		],
# 		"ind1":"8",
# 		"ind2":"\\"
# 	},
# 	"recordingEventRecordingNotes":{
# 		"tag":"500",
# 		"instructions":None,
# 		"subfields":[
# 			{
# 				"a":"value",
# 				"prefix":"Notes about the original analog recording: "
# 			}
# 		],
# 		"ind1":"\\",
# 		"ind2":"\\"
# 	},
# 	"recordingEventTitle":{
# 		"tag":"500",
# 		"instructions":None,
# 		"subfields":[
# 			{
# 				"a":"value",
# 				"prefix":"Title of event: "
# 			}
# 		],
# 		"ind1":"\\",
# 		"ind2":"\\"
# 	},
# 	"recordingLocation":{
# 		"tag":"500",
# 		"instructions":None,
# 		"subfields":[
# 			{
# 				"a":"value",
# 				"prefix":"Location of recording: "
# 			}
# 		],
# 		"ind1":"\\",
# 		"ind2":"\\"
# 	},
# 	"recordingPermissions":{
# 		"tag":"540",
# 		"instructions":None,
# 		"subfields":[
# 			{
# 				"a":"value"
# 			},
# 			{
# 				"c":"Speaker release form."
# 			}
# 		],
# 		"ind1":"\\",
# 		"ind2":"\\"
# 	},
# 	"recordingTapeNumber":{
# 		"tag":"500",
# 		"instructions":None,
# 		"subfields":[
# 			{
# 				"a":"value",
# 				"prefix":"Original audiocassette tape number: "
# 			}
# 		],
# 		"ind1":"\\",
# 		"ind2":"\\"
# 	},
# 	"FilmTitle":{
# 		"tag":"630",
# 		"instructions":"Parsed specifically in its own function",
# 		"subfields":[
# 			{
# 				"a":"value",
# 				"suffix":"(Motion Piction)"
# 			}
# 		],
# 		"ind1":"\\",
# 		"ind2":"4"
# 	},
# 	"Speaker":{
# 		"tag":"700",
# 		"instructions":"Parsed specifically in its own function",
# 		"subfields":[
# 			{
# 				"a":"value",
# 				"suffix":", "
# 			},
# 			{
# 				"e":"speaker"
# 			}
# 		],
# 		"ind1":"1",
# 		"ind2":"\\"
# 	},
# 	"duration":{
# 		"tag":"306",
# 		"instructions":"rawduration",
# 		"subfields":[],
# 		"ind1":"\\",
# 		"ind2":"\\"
# 	},
# 	"url":{
# 		"tag":"856",
# 		"instructions":None,
# 		"subfields":[
# 			{
# 				"z":"View item on Internet Archive"
# 			},
# 			{
# 				"u":"value"
# 			}
# 		],
# 		"ind1":"4",
# 		"ind2":"0"
# 	}
# }

def add_collection_defaults(Record):
	'''
	ADD COLLECTION-SPECIFIC DEFAULT FIELDS
	This is stuff applicable specifically to our CLIR project.
	Presumably this kind of set of fields could be adapted to any
	bulk creation of a collection-bound set of records.
	These are all streaming audio recordings digitized from tapes
	with very similar provenance, so there is a lot that is consistent
	across records for the entire collectoin.
	'''
	### 040
	ohFourOh = fields.DataField('040','\\','\\')
	for x in [
		fields.Subfield(
			'a',
			'CUY'
			),
		fields.Subfield(
			'b',
			'eng'
			),
		fields.Subfield(
			'e',
			'rda'
			),
		fields.Subfield(
			'c',
			'CUY'
			)
		]:
		ohFourOh.subfields.append(x)

	Record.dataFields.append(ohFourOh)

	### 110
	corpAuthor = fields.DataField('110','2','\\')
	for x in [
		fields.Subfield(
			'a',
			'Top Value Television (Production company), '
			),
		fields.Subfield(
			'e',
			'production company.'
			)
		]:
		corpAuthor.subfields.append(x)

	Record.dataFields.append(corpAuthor)

	### 264
	publication = fields.DataField('264','\\','1')
	for x in [
		fields.Subfield(
			'a',
			'Berkeley, California : '
			),
		fields.Subfield(
			'b',
			'UC Berkeley Art Museum and Pacific Film Archive ; '
			),
		fields.Subfield(
			'c',
			'2019.'
			)
		]:
		publication.subfields.append(x)

	Record.dataFields.append(publication)

	### 300
	physical = fields.DataField('300','\\','\\')
	for x in [
		fields.Subfield('a','1 online resource')
		]:
		physical.subfields.append(x)

	Record.dataFields.append(physical)

	### 336
	contentType = fields.DataField('336','\\','\\')
	for x in [
		fields.Subfield('a','two-dimensional moving image'),
		fields.Subfield('b','tdi'),
		fields.Subfield('2','rdacontent')
		]:
		contentType.subfields.append(x)

	Record.dataFields.append(contentType)

	### 337
	media = fields.DataField('337','\\','\\')
	for x in [
		fields.Subfield('a','computer'),
		fields.Subfield('2','rdamedia')
		]:
		media.subfields.append(x)

	Record.dataFields.append(media)

	### 338
	carrier = fields.DataField('338','\\','\\')
	for x in [
		fields.Subfield('a','online resource'),
		fields.Subfield('2','rdacarrier')
		]:
		carrier.subfields.append(x)

	Record.dataFields.append(carrier)

	### 344 type recording
	typerecording = fields.DataField('344','\\','\\')
	for x in [
		fields.Subfield('a','digital'),
		fields.Subfield('2','rdatr')
		]:
		typerecording.subfields.append(x)

	Record.dataFields.append(typerecording)

	### 344 channels
	channelSpec = Record.customProperties['MonoStereo']
	if (channelSpec and channelSpec != "unknown") :
		channels = fields.DataField('344','\\','\\')
		for x in [
			fields.Subfield('g',Record.customProperties['MonoStereo']),
			fields.Subfield('2','rdacpc')
			]:
			channels.subfields.append(x)

		Record.dataFields.append(channels)

	### 347 file type
	fType = fields.DataField('347','\\','\\')
	for x in [
		fields.Subfield('a','video file'),
		fields.Subfield('2','rdaft')
		]:
		fType.subfields.append(x)

	Record.dataFields.append(fType)

	### 347 bitrate
	# bitrate = fields.DataField('347','\\','\\')
	# bitrate.subfields.append(
	# 	fields.Subfield('f','variable bit rate 190-250 kbit/s')
	# 	)

	# Record.dataFields.append(bitrate)

	### 500 general pfa note
	pfanote = fields.DataField('500','\\','\\')
	pfanote.subfields.append(
		fields.Subfield(
			'a',
			("From the Top Value Television (TVTV) collection "
			"at UC Berkeley Art Museum and Pacific Film Archive. "
			"Digitized from open reel videotape in 2019 "
			"as part of a National Endowment for the Humanities "
			"Collections and Reference Resources grant project.")
			)
		)
	Record.dataFields.append(pfanote)

	### 542 copyright
	copyright = fields.DataField('542','\\','\\')
	copyright.subfields.append(
		fields.Subfield('a','All materials copyright TVTV.')
		)
	Record.dataFields.append(copyright)

	### 536
	funding = fields.DataField('536','\\','\\')
	funding.subfields.append(
		fields.Subfield('a',
		('Digitization made possible in part by funding from '
		'The National Endowment for the Humanities.')
		)
		)
	Record.dataFields.append(funding)

	### 530 additional physical form
	addForm = fields.DataField('530','\\','\\')
	for x in [
		fields.Subfield('a','Originally recorded on EIAJ 1/2" open-reel videotape.'),
		fields.Subfield('c','Access to original tape is restricted.')
		]:
		addForm.subfields.append(x)

	Record.dataFields.append(addForm)

	### 650 one subject?
	subject = fields.DataField('651','\\','0')
	for x in [
		fields.Subfield('a','United States'),
		fields.Subfield('x','Politics and government'),
		fields.Subfield('y','1972-1974')
		]:
		subject.subfields.append(x)

	Record.dataFields.append(subject)

	### 710 BAMPFA
	bampfa = fields.DataField('710','2','\\')
	for x in [
		fields.Subfield('a','UC Berkeley Art Museum and Pacific Film Archive, '),
		fields.Subfield('e','conservator')
		]:
		bampfa.subfields.append(x)
	Record.dataFields.append(bampfa)

	### 710 NEH
	clir = fields.DataField('710','2','\\')
	for x in [
		fields.Subfield('a','National Endowment for the Humanities, '),
		fields.Subfield('e','sponsor')
		]:
		clir.subfields.append(x)
	Record.dataFields.append(clir)

	### 949 wb
	web = fields.DataField('949','\\','1')
	for x in [
		fields.Subfield('l','wb')
		]:
		web.subfields.append(x)
	Record.dataFields.append(web)

	### 956 stats field
	stats = fields.DataField('956','\\','\\')
	for x in [
		fields.Subfield('a','20200901'),
		fields.Subfield('b','pfmcq'),
		fields.Subfield('c','CO')
		]:
		stats.subfields.append(x)
	Record.dataFields.append(stats)

	# ### 710 CLIR
	# clir = fields.DataField('710','2','\\')
	# for x in [
	# 	fields.Subfield('a','CLIR, '),
	# 	fields.Subfield('e','sponsoring body')
	# 	]:
	# 	clir.subfields.append(x)
	# Record.dataFields.append(clir)


###########################
###### HERE ARE SOME FUNCTIONS TO PARSE
###### DATA THAT IS SPECIFIC TO OUR TYPES OF RECORDS...
###### THEY CORRESPOND TO THE customProperties DICT
###### DEFINED IN THE `RECORD` CLASS
###### AND ALSO WE PARSE THE MARCmapper DICT ABOVE

def set_nonfiling_indicator(Record):
	title = None
	nonfiling = None
	for dataField in Record.dataFields:
		if dataField.tag == '245':
			titleField = dataField
			for subfield in dataField.subfields:
				if subfield.subfieldCharacter == 'a':
					title = subfield.value

	if title:
		if title.lower().startswith("the "):
			nonfiling = '4'
		elif title.lower().startswith("an "):
			nonfiling = '3'
		elif title.lower().startswith("a "):
			nonfiling = '2'

	if nonfiling:
		for dataField in Record.dataFields:
			if dataField.tag == '245':
				dataField.ind2 = nonfiling

	# return nonfiling

def set_duration(Record):
	duration = None
	if 'duration' in Record.fieldedData:
		duration = Record.fieldedData['duration']
		print(duration)
		for dataField in Record.dataFields:
			if dataField.tag == '300':
				for subfield in dataField.subfields:
					if subfield.subfieldCharacter == 'a':
						subfield.value = "{} ({})".format(subfield.value,duration)
						# print(subfield.value)
		hhmmss = duration.replace(":","")
		print(hhmmss)
		if len(hhmmss) < 6:
			hhmmss = hhmmss.zfill(6)
		threeOhSix = fields.DataField("306","\\","\\")
		threeOhSix.subfields.append(fields.Subfield('a',hhmmss))


		Record.dataFields.append(threeOhSix)




# def parse_ohOhEight_Dates(Record):
# 	year = Record.fieldedData['year']


def parse_speaker_names(Record):
	namesLNFN = Record.fieldedData['lnfn'].split('|')
	if namesLNFN != ['']:
		for name in namesLNFN:
			addedEntry = fields.DataField('700','1','\\',)
			for x in [
				fields.Subfield('a',name),
				fields.Subfield('e','speaker')
				]:
				addedEntry.subfields.append(x)
			Record.dataFields.append(addedEntry)
	speakers = Record.fieldedData['Speakers'].split('|')
	if speakers != ['']:
		titleProper = fields.DataField('245','0','0')
		date = Record.customProperties['yyyymmdd']
		try:
			if all([isinstance(int(d),int) for d in date]):
				dateFinal = "{}/{}/{}".format(date[:4],date[4:6],date[6:8])
		except:
			dateFinal = date
		for x in [
			fields.Subfield(
				'a',
				"[{}. Speaking at the Pacific Film Archive: {}.] /".format(
					', '.join(speakers),
					dateFinal
					)
				),
			fields.Subfield(
				'c',
				"UC Berkeley Art Museum and Pacific Film Archive."
				)
			]:
			titleProper.subfields.append(x)
		Record.dataFields.append(titleProper)

def parse_film_title_subjects(Record):
	titles = Record.fieldedData['FilmTitles'].split('|')
	if titles != ['']:
		for title in titles:
			subj = fields.DataField('630','\\','4')
			subj.subfields.append(
				fields.Subfield('a',title+" (Motion Picture)")
				)
			Record.dataFields.append(subj)

def parse_recording_date(Record):
	date = Record.fieldedData['recordingDate']
	try:
		# this is the date format from filemaker
		# CHECK FOR EITHER PST OR PDT!!!
		date = datetime.strptime(date,'%a %b %d %H:%M:%S PST %Y')
		yyyymmdd = datetime.strftime(date,'%Y%m%d')
		# print(date)#,yyyymmdd)
	except:
		try:
			date = datetime.strptime(date,'%a %b %d %H:%M:%S PDT %Y')
			yyyymmdd = datetime.strftime(date,'%Y%m%d')
		except:
			yyyymmdd = 'date unknown'

	Record.customProperties['yyyymmdd'] = yyyymmdd
	if len(Record.customProperties['yyyymmdd']) == 8:
		recDate = fields.DataField('033','0','0')
		for x in [
			fields.Subfield('a',Record.customProperties['yyyymmdd']),
			fields.Subfield('b','4360'),
			fields.Subfield('c','B5')
			]:
			recDate.subfields.append(x)
		Record.dataFields.append(recDate)

def parse_stereo_mono(Record):
	try:
		Record.customProperties['MonoStereo'] = Record.fieldedData['channels']
	except:
		# if the key doesn't exist
		Record.customProperties['MonoStereo'] = 'unknown'
	if not Record.customProperties['MonoStereo']:
		# if the key exists but it's empty
		Record.customProperties['MonoStereo'] = 'unknown'


def parse_duration(Record):
	try:
		Record.customProperties['duration'] = Record.fieldedData['duration']
	except:
		# leave duration = None
		pass
	if Record.customProperties['duration']:
		# parse it to seconds
		# parse that to HHMMSS
		# and put it in 306
		# and also customProp['time']
		# and also 300 $a
		pass

def set_ohOhSeven(Record,config):
	'''
	THESE VALUES ARE MOSTLY SET FOR THE PARTICULAR COLLECTION
	IN CONFIG.INI WITH ADD'L VALUES BASED ON RECORD SPECIFICS
	'''
	formatDict = ast.literal_eval(config['ohOhSeven']['ohOhSeven'])
	# channels = Record.customProperties['']

	if Record.customProperties['format'] == "REC":
		'''
		This is a collection of streaming digital audio
		'''
		channels = Record.customProperties['MonoStereo']
		if (channels and channels == "unknown"):
			e = "u"
		elif (channels and channels == "mono"):
			e = "m"
		elif (channels and channels == "stereo"):
			e = "s"
		elif (channels and channels == "surround"):
			e = "q"
		else:
			e = "\\"

		formatDict['e'] = e

	elif Record.customProperties['format'] == 'COM':
		# TVTV streaming files
		channels = Record.customProperties['MonoStereo']
		if (channels and channels == "unknown"):
			f = "u"
		elif (channels and channels in ["mono","stereo"]):
			f = "a"
		else:
			f = "u"

		formatDict['f'] = f

	else:
		return ''

	ohOhSevenObject = fields.OhOhSeven(
		**formatDict
		)
	return ohOhSevenObject.data.replace("\\","").replace("||","\\") # sleight of hand to account for empty $c

def main(Record):
	parse_stereo_mono(Record)
	# parse_recording_date(Record)
	# parse_speaker_names(Record)
	# parse_film_title_subjects(Record)
	# parse_duration(Record)
	add_collection_defaults(Record)
