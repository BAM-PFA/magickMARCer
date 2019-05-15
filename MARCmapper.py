#!/usr/bin/env python3
'''
Map field names from input to MARC tags
'''

MARCmapper = {
	"recordingDate":{
		"tag":None,
		"status":"rawdate",
		"subfields":{
			"":""
		}
	},
	"DigitizationNotes":{
		"tag":"500",
		"status":None,
		"subfields":{
			"a":"value"
		}
	},
	"recordingEventDescription":{
		"tag":"520",
		"status":None,
		"subfields":{
			"a":"value",
			"prepend":"Description of the event:",
		}
	},
	"recordingEventRecordingNotes":{
		"tag":"500",
		"status":None,
		"subfields":{
			"a":"value",
			"prepend":"Notes about the original analog recording:"
		}
	},
	"recordingEventTitle":{
		"tag":"500",
		"status":None,
		"subfields":{
			"a":"value",
			"prepend":"Title of event:"
		}
	},
	"recordingLocation":{
		"tag":"500",
		"status":None,
		"subfields":{
			"a":"value",
			"prepend":"Location of recording:"
		}
	},
	"recordingPermissions":{
		"tag":"540",
		"status":None,
		"subfields":{
			"a":"value",
			"c":"Speaker release form"
		}
	},
	"recordingTapeNumber":{
		"tag":"540",
		"status":None,
		"subfields":{
			"a":"value",
			"prepend":"Original audiocassette tape number:"
		}
	},
	"FilmTitle":{
		"tag":"630",
		"status":None,
		"subfields":{
			"a":"value",
			"suffix":"(Motion Piction)"
		}
	},
	"Speaker":{
		"tag":"700",
		"status":None,
		"subfields":{
			"a":"value",
			"suffix":", ",
			"e":"speaker"
		}
	},
	"duration":{
		"tag":"306",
		"status":"rawduration",
		"subfields":{
			"":""
		}
	},
	"DigitizationNotes":{
		"tag":"540",
		"status":None,
		"subfields":{
			"":""
		}
	},
	"DigitizationNotes":{
		"tag":"540",
		"status":None,
		"subfields":{
			"":""
		}
	}
}

def add_collection_defaults(Record):
	# ADD COLLECTION-SPECIFIC DEFAULT FIELDS
	#### 007
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

	### 264
	publication = fields.DataField('264','','1')
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

	self.dataFields.append(publication)

	### 336
	### 337
	media = fields.DataField('337','','')
	for x in [
		fields.Subfield('a','computer'),
		fields.Subfield('2','rdamedia')
		]:
		media.subfields.append(x)

	self.dataFields.append(media)

	### 338
	carrier = fields.DataField('338','','')
	for x in [
		fields.Subfield('a','online resource'),
		fields.Subfield('2','rdacarrier')
		]:
		carrier.subfields.append(x)

	self.dataFields.append(carrier)

	### 344 type recording
	typerecording = fields.DataField('344','','')
	for x in [
		fields.Subfield('a','digital'),
		fields.Subfield('2','rdatr')
		]:
		typerecording.subfields.append(x)

	self.dataFields.append(typerecording)

	### 344 channels
	channels = fields.DataField('344','','')
	for x in [
		fields.Subfield('g',self.MonoStereo),
		fields.Subfield('2','rdacpc')
		]:
		channels.subfields.append(x)

	self.dataFields.append(channels)

	### 347 file type
	fType = fields.DataField('347','','')
	for x in [
		fields.Subfield('a','audio file'),
		fields.Subfield('2','rdaft')
		]:
		fType.subfields.append(x)

	self.dataFields.append(fType)

	### 347 bitrate
	bitrate = fields.DataField('347','','')
	bitrate.subfields.append(
		fields.Subfield('f','variable bit rate 190-250 kbit/s')
		)

	self.dataFields.append(bitrate)

	### 500 general pfa note
	pfanote = fields.DataField('500','','')
	pfanote.subfields.append(
		fields.Subfield(
			'a',
			("Part of the Pacific Film Archive theater guest "
			"recording collection.... yadda yadda"
			"digitized from audiocassette in 2019 by MediaPreserve "
			"as part of a CLIR Recordings at Risk grant project")
			)
		)
	self.dataFields.append(pfanote)

	### 542 copyright
	copyright = fields.DataField('542','','')
	copyright.subfields.append('a','Boilerplate copyright statement TBD')
	self.dataFields.append(copyright)

	### 536
	funding = fields.DataField('536','','')
	funding.subfields.append(
		'a',
		('Digitization sponsored by a grant from the '
		'Council on Library and Information Resources')
		)
	self.dataFields.append(funding)

	### 530 additional physical form
	addForm = fields.DataField('530','','')
	for x in [
		fields.Subfield('a','Originally recorded on audio cassette.'),
		fields.Subfield('c','Access to original tape may be restricted.')
		]:
		addForm.subfields.append(x)

	self.dataFields.append(addForm)

	### 710 BAMPFA
	bampfa = fields.DataField('710','2','')
	for x in [
		fields.Subfield('a','UC Berkeley Art Museum and Pacific Film Archive, '),
		fields.Subfield('e','host institution')
		]:
		bampfa.subfields.append(x)
	self.dataFields.append(bampfa)

	### 710 CLIR
	clir = fields.DataField('710','2','')
	for x in [
		fields.Subfield('a','CLIR, '),
		fields.Subfield('e','sponsoring body')
		]:
		clir.subfields.append(x)
	self.dataFields.append(clir)