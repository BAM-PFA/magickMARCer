#!/usr/bin/env python3
import csv
from datetime import datetime
import json
import time

yyyymd = time.strftime("%Y%m%d")
yymmdd = time.strftime("%y%m%d")
fractionalNow = datetime.now().strftime("%Y%m%d%H%M%S.%f")[:-4]

class DataField:
		def __init__(
			self,
			tag,
			indicator1='',
			indicator2=''
			):
			self.tag = tag
			self.indicator1 = indicator1
			self.indicator2 = indicator2

			self.subfields = []

class Subfield:
	def __init__(self,subfieldCharacter,value):
		self.subfieldCharacter = subfieldCharacter
		self.value = value

class Leader:
	def __init__(self,ItemBytes):
		self.ItemBytes = ItemBytes

		self.data = (
			"{}"
			"{}"
			"{}"
			"{}"
			"{}"
			"{}"
			"{}"
			"{}"
			"{}"
			"{}"
			"{}"
			"{}"
			"{}"
			"{}"
			"{}"
			"{}".format(
				"00000", #  Record length (??)
				self.ItemBytes.Recstat,
				self.ItemBytes.Type,
				self.ItemBytes.BLvl,
				self.ItemBytes.Ctrl,
				"a", # character coding scheme (UTF-8)
				"2", # indicator count
				"2", # subfield count
				"00000", # Base Address of Data (system supplied???)
				self.ItemBytes.ELvl,
				self.ItemBytes.Desc,
				" ",
				"4", # Length of the length-of-field portion
				"5", # Length of the starting-character-position portion
				"0", # Length of the implementation-defined portion
				"0"  # Undefined
				)
			)

class OhOhEight:
	def __init__(self,ItemBytes):
		self.ItemBytes = ItemBytes

		self.data = (
			"{}"
			"{}"
			"{}"
			"{}"
			"{}"
			"{}"
			"{}"
			"{}"
			"{}".format(
				self.ItemBytes.Entered,
				self.ItemBytes.DtSt,
				self.ItemBytes.Dates[:4], # Date 1
				self.ItemBytes.Dates[4:], # Date 2
				self.ItemBytes.Ctry,
				self.ItemBytes.set_008_bytes(),
				self.ItemBytes.Lang,
				self.ItemBytes.MRec,
				self.ItemBytes.Srce
				)
			)

class OhOhSix:
	def __init__(self):
		pass


class ItemBytes:
	"""
	Manifestation-specific codes used in Leader/008/006
	format must be one of: BKS, CNR, COM, MAP, MIX, REC, SCO, VIS
	formatCode is the more specific MARC "type code"
	"""
	def __init__(
		self,
		format,
		AccM="      ",
		Alph=" ",
		Audn=" ",
		Biog=" ",
		BLvl=" ",
		Comp="  ",
		Conf=" ",
		Cont="    ",
		CrTp="a",
		Ctrl=" ",
		Ctry="   ",
		Dates="        ",
		Desc=" ",
		DtSt=" ",
		ELvl=" ",
		Entered=fractionalNow,
		EntW=" ",
		Fest=" ",
		File="u",
		FMus=" ",
		Form=" ",
		Freq=" ",
		GPub=" ",
		Ills="    ",
		Indx=" ",
		Lang="   ",
		LitF="u",
		LTxt="  ",
		MRec=" ",
		OCLC=None,
		Orig=" ",
		Part=" ",
		Proj="  ",
		Recstat="n",
		Regl=" ",
		Relf="    ",
		Replaced="                ",
		SpFm="  ",
		Srce="d",
		SrTp=" ",
		SL="0",
		Tech="n",
		Time="   ",
		TMat=" ",
		TrAr="n",
		Type=" "
		):
		self.format = format
		self.AccM=AccM
		self.Alph=Alph
		self.Audn=Audn
		self.Biog=Biog
		self.BLvl=BLvl
		self.Comp=Comp
		self.Conf=Conf
		self.Cont=Cont
		self.CrTp=CrTp
		self.Ctrl=Ctrl
		self.Ctry=Ctry
		self.Dates=Dates
		self.Desc=Desc
		self.DtSt=DtSt
		self.ELvl=ELvl
		self.Entered=Entered
		self.EntW=EntW
		self.Fest=Fest
		self.File=File
		self.FMus=FMus
		self.Form=Form
		self.Freq=Freq
		self.GPub=GPub
		self.Ills=Ills
		self.Indx=Indx
		self.Lang=Lang
		self.LitF=LitF
		self.LTxt=LTxt
		self.MRec=MRec
		self.OCLC=OCLC
		self.Orig=Orig
		self.Part=Part
		self.Proj=Proj
		self.Recstat=Recstat
		self.Regl=Regl
		self.Relf=Relf
		self.Replaced=Replaced
		self.SpFm=SpFm
		self.Srce=Srce
		self.SrTp=SrTp
		self.SL=SL
		self.Tech=Tech
		self.Time=Time
		self.TMat=TMat
		self.TrAr=TrAr
		self.Type=Type

	def set_008_bytes(self):
		"""
		Set the 008 format-specific 17 character byte string (positions 18-34)
		"""
		if self.format == "BKS":
			bytes = (
				"{}"
				"{}"
				"{}"
				"{}"
				"{}"
				"{}"
				"{}"
				"{}"
				"{}"
				"{}"
				"{}".format(
					self.Ills,
					self.Audn,
					self.Form,
					self.Cont,
					self.GPub,
					self.Conf,
					self.Fest,
					self.Indx,
					" ",
					self.LitF,
					self.Biog
					)
				)

		elif self.format == "REC":
			bytes = (
				"{}"
				"{}"
				"{}"
				"{}"
				"{}"
				"{}"
				"{}"
				"{}"
				"{}"
				"{}".format(
					self.Comp,
					self.FMus,
					self.Part,
					self.Audn,
					self.Form,
					self.AccM,
					self.LTxt,
					" ",
					self.TrAr,
					" "
					)
				)

		elif self.format == "VIS":
			bytes = (
				"{}"
				"{}"
				"{}"
				"{}"
				"{}"
				"{}"
				"{}"
				"{}"
				"{}"
				"{}"
				"{}"
				"{}"
				"{}"
				"{}"
				"{}".format(
					self.Time,
					" ",
					self.Audn,
					" ",
					" ",
					" ",
					" ",
					" ",
					self.GPub,
					self.Form,
					" ",
					" ",
					" ",
					self.TMat,
					self.Tech
					)
				)

		print(bytes)
		if len(bytes) == 17:
			return bytes
		else:
			return False


