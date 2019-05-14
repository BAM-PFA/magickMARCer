#!/usr/bin/env python3
import csv
from datetime import datetime
import json
import time

class Record:
	'''
	Take in a dict of fieldedData and parse out a MARC record in JSON....
	'''
	def __init__(
		self,
		fieldedData
		):

		self.fieldedData = fieldedData