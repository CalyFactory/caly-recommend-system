# -*- coding: utf-8 -*-
#from extractor.common import db_manager
import unittest
import event_extractor
import json

# python3 -m unittest -v testRecommendLocation.py

with open('../key/testcase.json') as tcJson:
	testcaseJs = json.load(tcJson)

class TestExtract(unittest.TestCase):
	# sentence,startDt, endDt
	def testLocation(self):
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N101"]["input"]["event_hashkey"],testcaseJs["N101"]["input"]["summary"],testcaseJs["N101"]["input"]["start_dt"],testcaseJs["N101"]["input"]["end_dt"],testcaseJs["N101"]["input"]["location"]), testcaseJs["N101"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["F001"]["input"]["event_hashkey"],testcaseJs["F001"]["input"]["summary"],testcaseJs["F001"]["input"]["start_dt"],testcaseJs["F001"]["input"]["end_dt"],testcaseJs["F001"]["input"]["location"]), testcaseJs["F001"]["result"])
		
	def testPurpose(self):
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N101"]["input"]["event_hashkey"],testcaseJs["N101"]["input"]["summary"],testcaseJs["N101"]["input"]["start_dt"],testcaseJs["N101"]["input"]["end_dt"],testcaseJs["N101"]["input"]["location"]), testcaseJs["N101"]["result"])

	def testTime(self):
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N101"]["input"]["event_hashkey"],testcaseJs["N101"]["input"]["summary"],testcaseJs["N101"]["input"]["start_dt"],testcaseJs["N101"]["input"]["end_dt"],testcaseJs["N101"]["input"]["location"]), testcaseJs["N101"]["result"])

	def failCase(self):
		pass