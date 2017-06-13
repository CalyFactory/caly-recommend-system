# -*- coding: utf-8 -*-
#from extractor.common import db_manager
import unittest
import event_extractor
import json

# python3 -m unittest -v testRecommendLocation.py

with open('../extractor/testcase.json') as tcJson:
	testcaseJs = json.load(tcJson)

class TestExtract(unittest.TestCase):
	def test_mixed(self):
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N10001"]["input"]["event_hashkey"],testcaseJs["N10001"]["input"]["summary"],testcaseJs["N10001"]["input"]["start_dt"],testcaseJs["N10001"]["input"]["end_dt"],testcaseJs["N10001"]["input"]["location"]), testcaseJs["N10001"]["result"])

	def test_location(self):
		"""
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N20101"]["input"]["event_hashkey"],testcaseJs["N20101"]["input"]["summary"],testcaseJs["N20101"]["input"]["start_dt"],testcaseJs["N20101"]["input"]["end_dt"],testcaseJs["N20101"]["input"]["location"]), testcaseJs["N20101"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N20201"]["input"]["event_hashkey"],testcaseJs["N20201"]["input"]["summary"],testcaseJs["N20201"]["input"]["start_dt"],testcaseJs["N20201"]["input"]["end_dt"],testcaseJs["N20201"]["input"]["location"]), testcaseJs["N20201"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N20301"]["input"]["event_hashkey"],testcaseJs["N20301"]["input"]["summary"],testcaseJs["N20301"]["input"]["start_dt"],testcaseJs["N20301"]["input"]["end_dt"],testcaseJs["N20301"]["input"]["location"]), testcaseJs["N20301"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N20401"]["input"]["event_hashkey"],testcaseJs["N20401"]["input"]["summary"],testcaseJs["N20401"]["input"]["start_dt"],testcaseJs["N20401"]["input"]["end_dt"],testcaseJs["N20401"]["input"]["location"]), testcaseJs["N20401"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N20402"]["input"]["event_hashkey"],testcaseJs["N20402"]["input"]["summary"],testcaseJs["N20402"]["input"]["start_dt"],testcaseJs["N20402"]["input"]["end_dt"],testcaseJs["N20402"]["input"]["location"]), testcaseJs["N20402"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N20501"]["input"]["event_hashkey"],testcaseJs["N20501"]["input"]["summary"],testcaseJs["N20501"]["input"]["start_dt"],testcaseJs["N20501"]["input"]["end_dt"],testcaseJs["N20501"]["input"]["location"]), testcaseJs["N20501"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N21101"]["input"]["event_hashkey"],testcaseJs["N21101"]["input"]["summary"],testcaseJs["N21101"]["input"]["start_dt"],testcaseJs["N21101"]["input"]["end_dt"],testcaseJs["N21101"]["input"]["location"]), testcaseJs["N21101"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N21201"]["input"]["event_hashkey"],testcaseJs["N21201"]["input"]["summary"],testcaseJs["N21201"]["input"]["start_dt"],testcaseJs["N21201"]["input"]["end_dt"],testcaseJs["N21201"]["input"]["location"]), testcaseJs["N21201"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N21301"]["input"]["event_hashkey"],testcaseJs["N21301"]["input"]["summary"],testcaseJs["N21301"]["input"]["start_dt"],testcaseJs["N21301"]["input"]["end_dt"],testcaseJs["N21301"]["input"]["location"]), testcaseJs["N21301"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N21401"]["input"]["event_hashkey"],testcaseJs["N21401"]["input"]["summary"],testcaseJs["N21401"]["input"]["start_dt"],testcaseJs["N21401"]["input"]["end_dt"],testcaseJs["N21401"]["input"]["location"]), testcaseJs["N21401"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N21501"]["input"]["event_hashkey"],testcaseJs["N21501"]["input"]["summary"],testcaseJs["N21501"]["input"]["start_dt"],testcaseJs["N21501"]["input"]["end_dt"],testcaseJs["N21501"]["input"]["location"]), testcaseJs["N21501"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N22101"]["input"]["event_hashkey"],testcaseJs["N22101"]["input"]["summary"],testcaseJs["N22101"]["input"]["start_dt"],testcaseJs["N22101"]["input"]["end_dt"],testcaseJs["N22101"]["input"]["location"]), testcaseJs["N22101"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N22201"]["input"]["event_hashkey"],testcaseJs["N22201"]["input"]["summary"],testcaseJs["N22201"]["input"]["start_dt"],testcaseJs["N22201"]["input"]["end_dt"],testcaseJs["N22201"]["input"]["location"]), testcaseJs["N22201"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N22301"]["input"]["event_hashkey"],testcaseJs["N22301"]["input"]["summary"],testcaseJs["N22301"]["input"]["start_dt"],testcaseJs["N22301"]["input"]["end_dt"],testcaseJs["N22301"]["input"]["location"]), testcaseJs["N22301"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N22401"]["input"]["event_hashkey"],testcaseJs["N22401"]["input"]["summary"],testcaseJs["N22401"]["input"]["start_dt"],testcaseJs["N22401"]["input"]["end_dt"],testcaseJs["N22401"]["input"]["location"]), testcaseJs["N22401"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N22501"]["input"]["event_hashkey"],testcaseJs["N22501"]["input"]["summary"],testcaseJs["N22501"]["input"]["start_dt"],testcaseJs["N22501"]["input"]["end_dt"],testcaseJs["N22501"]["input"]["location"]), testcaseJs["N22501"]["result"])
		"""
		
	def test_purpose(self):
		"""
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N30101"]["input"]["event_hashkey"],testcaseJs["N30101"]["input"]["summary"],testcaseJs["N30101"]["input"]["start_dt"],testcaseJs["N30101"]["input"]["end_dt"],testcaseJs["N30101"]["input"]["location"]), testcaseJs["N30101"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N30201"]["input"]["event_hashkey"],testcaseJs["N30201"]["input"]["summary"],testcaseJs["N30201"]["input"]["start_dt"],testcaseJs["N30201"]["input"]["end_dt"],testcaseJs["N30201"]["input"]["location"]), testcaseJs["N30201"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N30301"]["input"]["event_hashkey"],testcaseJs["N30301"]["input"]["summary"],testcaseJs["N30301"]["input"]["start_dt"],testcaseJs["N30301"]["input"]["end_dt"],testcaseJs["N30301"]["input"]["location"]), testcaseJs["N30301"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N30401"]["input"]["event_hashkey"],testcaseJs["N30401"]["input"]["summary"],testcaseJs["N30401"]["input"]["start_dt"],testcaseJs["N30401"]["input"]["end_dt"],testcaseJs["N30401"]["input"]["location"]), testcaseJs["N30401"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N30501"]["input"]["event_hashkey"],testcaseJs["N30501"]["input"]["summary"],testcaseJs["N30501"]["input"]["start_dt"],testcaseJs["N30501"]["input"]["end_dt"],testcaseJs["N30501"]["input"]["location"]), testcaseJs["N30501"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N30601"]["input"]["event_hashkey"],testcaseJs["N30601"]["input"]["summary"],testcaseJs["N30601"]["input"]["start_dt"],testcaseJs["N30601"]["input"]["end_dt"],testcaseJs["N30601"]["input"]["location"]), testcaseJs["N30601"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N31101"]["input"]["event_hashkey"],testcaseJs["N31101"]["input"]["summary"],testcaseJs["N31101"]["input"]["start_dt"],testcaseJs["N31101"]["input"]["end_dt"],testcaseJs["N31101"]["input"]["location"]), testcaseJs["N31101"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N31201"]["input"]["event_hashkey"],testcaseJs["N31201"]["input"]["summary"],testcaseJs["N31201"]["input"]["start_dt"],testcaseJs["N31201"]["input"]["end_dt"],testcaseJs["N31201"]["input"]["location"]), testcaseJs["N31201"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N31301"]["input"]["event_hashkey"],testcaseJs["N31301"]["input"]["summary"],testcaseJs["N31301"]["input"]["start_dt"],testcaseJs["N31301"]["input"]["end_dt"],testcaseJs["N31301"]["input"]["location"]), testcaseJs["N31301"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N31401"]["input"]["event_hashkey"],testcaseJs["N31401"]["input"]["summary"],testcaseJs["N31401"]["input"]["start_dt"],testcaseJs["N31401"]["input"]["end_dt"],testcaseJs["N31401"]["input"]["location"]), testcaseJs["N31401"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N31501"]["input"]["event_hashkey"],testcaseJs["N31501"]["input"]["summary"],testcaseJs["N31501"]["input"]["start_dt"],testcaseJs["N31501"]["input"]["end_dt"],testcaseJs["N31501"]["input"]["location"]), testcaseJs["N31501"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N31601"]["input"]["event_hashkey"],testcaseJs["N31601"]["input"]["summary"],testcaseJs["N31601"]["input"]["start_dt"],testcaseJs["N31601"]["input"]["end_dt"],testcaseJs["N31601"]["input"]["location"]), testcaseJs["N31601"]["result"])
		"""

	def test_time(self):
		
		#self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N40101"]["input"]["event_hashkey"],testcaseJs["N40101"]["input"]["summary"],testcaseJs["N40101"]["input"]["start_dt"],testcaseJs["N40101"]["input"]["end_dt"],testcaseJs["N40101"]["input"]["location"]), testcaseJs["N40101"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N40201"]["input"]["event_hashkey"],testcaseJs["N40201"]["input"]["summary"],testcaseJs["N40201"]["input"]["start_dt"],testcaseJs["N40201"]["input"]["end_dt"],testcaseJs["N40201"]["input"]["location"]), testcaseJs["N40201"]["result"])
		"""
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N40301"]["input"]["event_hashkey"],testcaseJs["N40301"]["input"]["summary"],testcaseJs["N40301"]["input"]["start_dt"],testcaseJs["N40301"]["input"]["end_dt"],testcaseJs["N40301"]["input"]["location"]), testcaseJs["N40301"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N40401"]["input"]["event_hashkey"],testcaseJs["N40401"]["input"]["summary"],testcaseJs["N40401"]["input"]["start_dt"],testcaseJs["N40401"]["input"]["end_dt"],testcaseJs["N40401"]["input"]["location"]), testcaseJs["N40401"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N40501"]["input"]["event_hashkey"],testcaseJs["N40501"]["input"]["summary"],testcaseJs["N40501"]["input"]["start_dt"],testcaseJs["N40501"]["input"]["end_dt"],testcaseJs["N40501"]["input"]["location"]), testcaseJs["N40501"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N41101"]["input"]["event_hashkey"],testcaseJs["N41101"]["input"]["summary"],testcaseJs["N41101"]["input"]["start_dt"],testcaseJs["N41101"]["input"]["end_dt"],testcaseJs["N41101"]["input"]["location"]), testcaseJs["N41101"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N41201"]["input"]["event_hashkey"],testcaseJs["N41201"]["input"]["summary"],testcaseJs["N41201"]["input"]["start_dt"],testcaseJs["N41201"]["input"]["end_dt"],testcaseJs["N41201"]["input"]["location"]), testcaseJs["N41201"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N41301"]["input"]["event_hashkey"],testcaseJs["N41301"]["input"]["summary"],testcaseJs["N41301"]["input"]["start_dt"],testcaseJs["N41301"]["input"]["end_dt"],testcaseJs["N41301"]["input"]["location"]), testcaseJs["N41301"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N41401"]["input"]["event_hashkey"],testcaseJs["N41401"]["input"]["summary"],testcaseJs["N41401"]["input"]["start_dt"],testcaseJs["N41401"]["input"]["end_dt"],testcaseJs["N41401"]["input"]["location"]), testcaseJs["N41401"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N41501"]["input"]["event_hashkey"],testcaseJs["N41501"]["input"]["summary"],testcaseJs["N41501"]["input"]["start_dt"],testcaseJs["N41501"]["input"]["end_dt"],testcaseJs["N41501"]["input"]["location"]), testcaseJs["N41501"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["N42001"]["input"]["event_hashkey"],testcaseJs["N42001"]["input"]["summary"],testcaseJs["N42001"]["input"]["start_dt"],testcaseJs["N42001"]["input"]["end_dt"],testcaseJs["N42001"]["input"]["location"]), testcaseJs["N42001"]["result"])
		"""
		

	def test_fail_case(self):
		"""
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["F001"]["input"]["event_hashkey"],testcaseJs["F001"]["input"]["summary"],testcaseJs["F001"]["input"]["start_dt"],testcaseJs["F001"]["input"]["end_dt"],testcaseJs["F001"]["input"]["location"]), testcaseJs["F001"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["F002"]["input"]["event_hashkey"],testcaseJs["F002"]["input"]["summary"],testcaseJs["F002"]["input"]["start_dt"],testcaseJs["F002"]["input"]["end_dt"],testcaseJs["F002"]["input"]["location"]), testcaseJs["F002"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["F003"]["input"]["event_hashkey"],testcaseJs["F003"]["input"]["summary"],testcaseJs["F003"]["input"]["start_dt"],testcaseJs["F003"]["input"]["end_dt"],testcaseJs["F003"]["input"]["location"]), testcaseJs["F003"]["result"])
		self.assertEqual(event_extractor.extract_info_from_event(testcaseJs["F004"]["input"]["event_hashkey"],testcaseJs["F004"]["input"]["summary"],testcaseJs["F004"]["input"]["start_dt"],testcaseJs["F004"]["input"]["end_dt"],testcaseJs["F004"]["input"]["location"]), testcaseJs["F004"]["result"])
		"""