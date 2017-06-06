from common import db_manager
from common.util import utils

from reinforce import Reinforce
import unittest
import pprint


import json 

with open('./testData.json') as test_data:
	test_data = json.load(test_data)
with open('./expectedData.json') as expected_data:
	expected_data = json.load(expected_data)	




class TestReinForce(unittest.TestCase):

	def test_hasAll(self):		
		print("==================01================")
		has_all = test_data["hasAll"]
		has_all_expected = expected_data["hasAllExpected"]
		reinforce = Reinforce(has_all)
		pprint.pprint("1.hasAll result => "+str(reinforce.event_reco_result))		
		self.assertEqual(reinforce.event_reco_result, has_all_expected)	

	def test_noLocation_no_event_type(self):	 		
		print("==================02================")
		noLocation_no_event_type = test_data["noLocationNoEventType"]
		noLocation_no_event_type_expected = expected_data["noLocationNoEventTypeExpected"]
		reinforce = Reinforce(noLocation_no_event_type)			
		pprint.pprint("2. noLocationNoEventType result => "+str(reinforce.event_reco_result))
		self.assertEqual(reinforce.event_reco_result, noLocation_no_event_type_expected)	
		
	def test_no_location_has_event_type(self):
		print("==================03================")
		noLocation_has_event_type = test_data["noLocationHasEventType"]
		noLocation_has_event_type_expected = expected_data["noLocationHasEventTypeExpected"]

		reinforce = Reinforce(noLocation_has_event_type)			
		pprint.pprint("3. noLocationHasEventType result => "+str(reinforce.event_reco_result))
		self.assertEqual(reinforce.event_reco_result, noLocation_has_event_type_expected)

	def test_has_location_no_event_type(self):
		print("==================04================")
		hasLocation_no_event_type = test_data["hasLocationNoEventType"]
		hasLocation_no_event_type_expected = expected_data["hasLocationNoEventTypeExpected"]		
		reinforce = Reinforce(hasLocation_no_event_type)			
		pprint.pprint("4. hasLocationNoEventType result => "+str(reinforce.event_reco_result))
		self.assertEqual(reinforce.event_reco_result, hasLocation_no_event_type_expected)			


if __name__ == '__main__':
	unittest.main()



# 1 위와 같은 방식이 맞는지..  펑션마다 확인해야하는지
# 2 input json파일 어떻게 넣는지.. 내가 하려는 방식이 맞는지
# 3 예상값이 random하게 나오는데 type만 확인하는방법이나. 

# instance.check_location_validation()