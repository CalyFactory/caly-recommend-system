# -*- coding: utf-8 -*-
#from extractor.common import db_manager
import unittest
import event_extractor
import json

# python3 -m unittest -v testRecommendLocation.py

with open('./common//key/testcase.json') as tcJson:
	testcaseJs = json.load(tcJson)

class TestExtract(unittest.TestCase):
	# sentence,startDt, endDt
	def testLocation(self):
		self.assertTrue(event_extractor.extract_info_from_event('성신여대 미팅','2017-07-04 12:00:00','2017-07-04 13:00:00',''), testcaseJs["101"])

# Testcase 1 : all
#testAnalysis('3275008b3da8adf4874f6e09cc127c75cf46711b3031cdebd1db9a29')
# Testcase 2 : without purpose
#testAnalysis('907d71d0b0809116217205674096ec15929c1dbe5afa9057d98cd439')
# Testcase 3 : without extractTime
#recommendLocation.testAnalysis('af0b3b5e551180310106982d9c94786507e397236cf93f345011850f')
# Testcase 4 : without location
#testAnalysis('217f53d8b6511daaf659f2911872a72b8be22c39c27714e3e2859f0e')