import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from reco import Reco 
import math
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

    """
    test_region_filter_1
    특정 지역을 넣고 해당하는 지역만 나오는지 체크

    input : 
        지역 : 신사역 
    output : 
        신사역에 해당하는 지역

    assert 내용
        1. exptected output의 recohashkey가 output안에 들어있는가
        2. exptected output의 갯수와 output의 결과가 같은가

    """
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
                

    """
    test_region_filter_2
    특정 지역을 넣고 해당하는 지역만 나오는지 체크

    input : 
        지역 : 건대입구역 
    output : 
        건대입구역에 해당하는 지역

    assert 내용
        1. exptected output의 recohashkey가 output안에 들어있는가
        2. exptected output의 갯수와 output의 결과가 같은가

    """
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
    

    """
    test_region_filter_3
    특정 지역을 넣고 해당하는 지역만 나오는지 체크

    input : 
        지역 : 잠실새내역, 국회의사당역  
    output : 
        잠실새내역, 국회의사당역에 해당하는 지역

    assert 내용
        1. exptected output의 recohashkey가 output안에 들어있는가
        2. exptected output의 갯수와 output의 결과가 같은가

    """
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

    """
    test_region_filter_4
    특정 지역을 넣고 해당하는 지역만 나오는지 체크

    input : 
        지역 : 없음   
    output : 
        빈 리스트

    assert 내용
        1. exptected output의 recohashkey가 output안에 들어있는가
        2. exptected output의 갯수와 output의 결과가 같은가

    """
    def test_region_filter_4(self):
        print_test_info()
        reco = Reco(
            test_data['test_region_filter_4']['input'],
            '',
            item_data = test_item_data
        )
        recoList = reco.get_reco_list()
        expectedList = test_data['test_region_filter_4']['output']
        

        for category in expectedList:
            for row in expectedList[category]:
                self.assertTrue(
                    row['reco_hashkey'] in [data['reco_hashkey'] for data in recoList[category]]
                )
            self.assertEqual(
                len(expectedList[category]),
                len(recoList[category])
            )

    """
    test_region_filter_5
    특정 지역을 넣고 해당하는 지역만 나오는지 체크

    input : 
        지역 : 소마역(디비에 없는 지역)   
    output : 
        빈 리스트

    assert 내용
        1. exptected output의 recohashkey가 output안에 들어있는가
        2. exptected output의 갯수와 output의 결과가 같은가

    """
    def test_region_filter_5(self):
        print_test_info()
        reco = Reco(
            test_data['test_region_filter_5']['input'],
            '',
            item_data = test_item_data
        )
        recoList = reco.get_reco_list()
        expectedList = test_data['test_region_filter_5']['output']
        

        for category in expectedList:
            for row in expectedList[category]:
                self.assertTrue(
                    row['reco_hashkey'] in [data['reco_hashkey'] for data in recoList[category]]
                )
            self.assertEqual(
                len(expectedList[category]),
                len(recoList[category])
            )


    """
    test_score_region_1
    특정 지역목록을 넣고 score의 장소 점수가 지역 순위에 맞게 계산되는지 테스트 

    input : 
        지역 : 신사역, 건대입구역  
    output : 
        신사역 목록 -> 십만자리의수가 '9'
        건대입구역 목록 -> 십만자리의수가 '8'

    assert 내용
        1. exptected output의 recohashkey가 output안에 들어있는가
        2. exptected output의 갯수와 output의 결과가 같은가
        3. output의 score의 십만자리수와 expected output의 십만자리수가 같은지

    """
    def test_score_region_1(self):
        print_test_info()
        reco = Reco(
            test_data['test_score_region_1']['input'],
            '',
            item_data = test_item_data
        )
        recoList = reco.get_reco_list()
        expectedList = test_data['test_score_region_1']['output']

        for category in expectedList:
            for row in expectedList[category]:
                self.assertTrue(
                    row['reco_hashkey'] in [data['reco_hashkey'] for data in recoList[category]]
                )
                recoItem = None
                for recoItem in recoList[category]:
                    if row['reco_hashkey'] == recoItem['reco_hashkey']:
                        break
                self.assertTrue(
                    recoItem is not None
                )
                for i in range(0, len(row['score'])):
                    if row['score'][i] == -1:
                        continue
                    self.assertEqual(
                        row['score'][i],
                        int((recoItem['score'] % math.pow(10, 6-i)) / math.pow(10, 5-i))
                    )
            self.assertEqual(
                len(expectedList[category]),
                len(recoList[category])
            )
    

    """
    test_score_region_1
    특정 지역목록과 예상목적을 넣고 score의 목적 점수가 목적 순위에 맞게 계산되는지 테스트 

    input : 
        지역 : 신사역, 건대입구역  
        목적 : CPI01, CPI02
    output : 
        신사역 목록 -> 만자리의수가 score 공식으로 계산된 목적점수이어야함
        건대입구역 목록 -> 만자리의수가 score 공식으로 계산된 목적점수이어야함

    assert 내용
        1. exptected output의 recohashkey가 output안에 들어있는가
        2. exptected output의 갯수와 output의 결과가 같은가
        3. output의 score의 만자리수와 expected output의 만자리수가 같은지

    """
    def test_score_purpose_1(self):
        print_test_info()
        reco = Reco(
            test_data['test_score_purpose_1']['input'],
            '',
            item_data = test_item_data
        )
        recoList = reco.get_reco_list()
        expectedList = test_data['test_score_purpose_1']['output']

        for category in expectedList:
            for row in expectedList[category]:

                self.assertTrue(
                    row['reco_hashkey'] in [data['reco_hashkey'] for data in recoList[category]]
                )
                recoItem = None
                for recoItem in recoList[category]:
                    if row['reco_hashkey'] == recoItem['reco_hashkey']:
                        break
                self.assertTrue(
                    recoItem is not None
                )
                for i in range(0, len(row['score'])):
                    if row['score'][i] == -1:
                        continue
                    self.assertEqual(
                        row['score'][i],
                        int((recoItem['score'] % math.pow(10, 6-i)) / math.pow(10, 5-i))
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
	unittest.main(argv=[sys.argv[0]])