import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from reco import Reco 
import unittest
import json

with open('./jsonData.json') as file:
    json_data = json.load(file)

with open('./testData.json') as file:
    test_data = json.load(file)

with open('./testItemData.json') as file:
    test_item_data = json.load(file)



def print_test_info():
    print(
        "\n%s : " % sys._getframe(1).f_code.co_name, 
        end='', 
        flush=True
    )

# test case 
class TestReco(unittest.TestCase):
    def test_helloworld(self):
        print_test_info()
        a = 1
        b = 1
        expected_result = 2
        self.assertEqual(a + b, expected_result)

    def test_helloworld2(self):
        print_test_info()
        a = 1
        b = 1
        expected_result = 2
        self.assertEqual(a + b, expected_result)

    def test_helloworld3(self):
        print_test_info()
        a = 1
        b = 1
        expected_result = 2
        self.assertEqual(a + b, expected_result)
    
    def test_region_filter_1(self):
        print_test_info()
        reco = Reco(
            test_data['test_region_filter_1']['input'],
            '',
            item_data = test_item_data
        )
        recoList = reco.get_reco_list()
        expectedList = test_data['test_region_filter_1']['output']
        
        for category in expectedList:
            for row in expectedList[category]:
                self.assertTrue(
                    row['reco_hashkey'] in [data['reco_hashkey'] for data in recoList[category]]
                )
            self.assertEqual(
                len(expectedList[category]),
                len(recoList[category])
            )
                
    def test_region_filter_2(self):
        print_test_info()
        reco = Reco(
            test_data['test_region_filter_2']['input'],
            '',
            item_data = test_item_data
        )
        recoList = reco.get_reco_list()
        expectedList = test_data['test_region_filter_2']['output']
        

        for category in expectedList:
            for row in expectedList[category]:
                self.assertTrue(
                    row['reco_hashkey'] in [data['reco_hashkey'] for data in recoList[category]]
                )
            self.assertEqual(
                len(expectedList[category]),
                len(recoList[category])
            )
    
    def test_region_filter_3(self):
        print_test_info()
        reco = Reco(
            test_data['test_region_filter_3']['input'],
            '',
            item_data = test_item_data
        )
        recoList = reco.get_reco_list()
        expectedList = test_data['test_region_filter_3']['output']
        

        for category in expectedList:
            for row in expectedList[category]:
                self.assertTrue(
                    row['reco_hashkey'] in [data['reco_hashkey'] for data in recoList[category]]
                )
            self.assertEqual(
                len(expectedList[category]),
                len(recoList[category])
            )

    


# 테스트에 사용될 데이터 만드는 함수. 테스트 케이스는 아니고, db의 추천 데이터를 json파일로 만듬
def save_all_recommend_item():
    reco = Reco(json_data, show_external_data = False)
    all_list = reco.get_all_list()

    print(
        json.dumps(
            all_list,
            indent = 4,
            sort_keys=True,
            ensure_ascii=False
        )
    )

    with open('testItemData.json', 'w') as outfile:
        json.dump(all_list, outfile, indent = 4)

    with open('testItemDataEncoded.json', 'w') as outfile:
        json.dump(all_list, outfile, indent = 4, ensure_ascii=False)

# 테스트 실행
if __name__ == '__main__':
	unittest.main()