

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))



os.environ["CALY_DB_CONF"] = "../key/conf.json"

from common import db_manager
from common.util import utils
from reco.reco import Reco
from reinforce import Reinforce
import unittest
import pprint


import json 

with open('./testData.json') as test_data:
	test_data = json.load(test_data)
with open('./expectedData.json') as expected_data:
	expected_data = json.load(expected_data)	




class TestReinForce(unittest.TestCase):

	def test_ret10(self):		
		print("==================01================")
		ret10 = test_data["ret10"]
		ret10_expected = expected_data["ret10"]
		reinforce = Reinforce(ret10)
		pprint.pprint("1.ret10 result => "+str(reinforce.event_reco_result["event_info_data"]))		
		self.assertEqual(reinforce.event_reco_result, ret10_expected)	
		# reoco = Reco(reinforce.event_reco_result["event_info_data"])
		# print(reoco.get_reco_list())
		

	def test_ret11(self):	 		
		print("==================02================")
		ret11 = test_data["ret11"]
		ret11_expected = expected_data["ret11"]
		reinforce = Reinforce(ret11)			
		pprint.pprint("2. ret11 result => "+str(reinforce.event_reco_result))
		self.assertEqual(reinforce.event_reco_result, ret11_expected)	
		
	def test_ret20(self):
		print("==================03================")
		ret20 = test_data["ret20"]
		ret20_expected = expected_data["ret20"]
		reinforce = Reinforce(ret20)			
		pprint.pprint("3. ret20 result => "+str(reinforce.event_reco_result))
		self.assertEqual(reinforce.event_reco_result, ret20_expected)

	def test_ret30(self):
		print("==================04================")
		ret30 = test_data["ret30"]
		ret30_expected = expected_data["ret30"]		
		reinforce = Reinforce(ret30)			
		pprint.pprint("4. ret30 result => "+str(reinforce.event_reco_result))
		self.assertEqual(reinforce.event_reco_result, ret30_expected)			

	def test_ret31(self):
		print("==================05================")
		ret31 = test_data["ret31"]
		ret31_expected = expected_data["ret31"]		
		reinforce = Reinforce(ret31)			
		pprint.pprint("5. ret31 result => "+str(reinforce.event_reco_result))
		self.assertEqual(reinforce.event_reco_result, ret31_expected)					
	
	def test_ret40(self):
		print("==================06================")
		ret40 = test_data["ret40"]
		ret40_expected = expected_data["ret40"]		
		reinforce = Reinforce(ret40)			
		pprint.pprint("6. ret40 result => "+str(reinforce.event_reco_result))
		self.assertEqual(reinforce.event_reco_result, ret40_expected)							
	
	def test_ret50(self):
		print("==================07================")
		ret50 = test_data["ret50"]
		ret50_expected = expected_data["ret50"]		
		reinforce = Reinforce(ret50)			
		pprint.pprint("7. ret50 result => "+str(reinforce.event_reco_result))
		self.assertEqual(reinforce.event_reco_result, ret50_expected)									


if __name__ == '__main__':
	unittest.main()



# 1 위와 같은 방식이 맞는지..  펑션마다 확인해야하는지
# 2 input json파일 어떻게 넣는지.. 내가 하려는 방식이 맞는지
# 3 예상값이 random하게 나오는데 type만 확인하는방법이나. 

# instance.check_location_validation()