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