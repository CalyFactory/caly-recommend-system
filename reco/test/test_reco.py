import os
import sys
os.environ["CALY_DB_CONF"] = "../key/conf.json"

from reco.reco import Reco 
import math
import unittest
import json

with open('./test_data/jsonData.json') as file:
    json_data = json.load(file)

with open('./test_data/testData.json') as file:
    test_data = json.load(file)

with open('./test_data/testItemData.json') as file:
    test_item_data = json.load(file)



def print_test_info():
    print(
        "\n%s : " % sys._getframe(1).f_code.co_name, 
        end='', 
        flush=True
    )

# test case 
class TestReco(unittest.TestCase):

    """
    동작 확인용 샘플 코드
    """
    def test_helloworld(self):
        print_test_info()
        a = 1
        b = 1
        expected_result = 2
        self.assertEqual(
            a + b, 
            expected_result
        )
        self.assertTrue(
            a + b == expected_result
        )
    """
    def test_db(self):
        reco = Reco(
            test_data['test_load_all']['input'],
            True,
            user_click = {
                "property_romantic": 70,
                "property_active_dynamic": 18,
                "property_active_static": 22,
                "property_food_korean": 9,
                "property_food_chinese": 10,
                "property_food_japanese": 11,
                "property_food_italian": 12,
                "all": 120
                
            }
        )
        recoList = reco.get_all_list()
        expectedList = test_item_data
        
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
    """
    test_load_all
    get_all_list()함수로 모든 데이터를 불러올 수 있는지 테스트

    input : 
        없음
    output : 
        저장된 모든 데이터

    assert 내용
        1. exptected output의 recohashkey가 output안에 들어있는가
        2. exptected output의 갯수와 output의 결과가 같은가

    """
    def test_load_all(self):
        print_test_info()
        reco = Reco(
            test_data['test_load_all']['input'],
            '',
            external_data = {
                'item_data': test_item_data,
                'user_click':None
            }
        )
        recoList = reco.get_all_list()
        expectedList = test_item_data
        
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
    test_load_all_null
    get_all_list()함수로 모든 데이터를 불러올 수 있는지 테스트

    input : 
        없음
    output : 
        저장된 모든 데이터

    assert 내용
        1. exptected output의 recohashkey가 output안에 들어있는가
        2. exptected output의 갯수와 output의 결과가 같은가

    """
    def test_load_all_null(self):
        print_test_info()
        reco = Reco(
            test_data['test_load_all_null']['input'],
            '',
            external_data = {
                'item_data': test_item_data,
                'user_click': None
            }
        )
        recoList = reco.get_all_list()
        expectedList = test_item_data
        
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
    test_load_all_external_1
    get_all_list()함수로 모든 데이터를 불러올 수 있는지 테스트
    show_external_data 파라미터를 true로 설정해 reco_hashkey 이외의 데이터도 나오는지 테스트

    input : 
        없음
    output : 
        저장된 모든 데이터

    assert 내용
        1. exptected output의 recohashkey가 output안에 들어있는가
        2. exptected output의 갯수와 output의 결과가 같은가

    """
    def test_load_all_external_1(self):
        print_test_info()
        reco = Reco(
            test_data['test_region_filter_1']['input'],
            show_external_data = True, 
            external_data = {
                'item_data': test_item_data,
                'user_click': None
            }
        )
        recoList = reco.get_reco_list()
        expectedList = test_data['test_region_filter_1']['output']
        
        for category in expectedList:
            for row in recoList[category]:
                self.assertNotEqual(
                    1,
                    len(row)
                )

            for row in expectedList[category]:
                self.assertTrue(
                    row['reco_hashkey'] in [data['reco_hashkey'] for data in recoList[category]]
                )
            self.assertEqual(
                len(expectedList[category]),
                len(recoList[category])
            ) 

    """ 
    test_load_all_external_2
    get_all_list()함수로 모든 데이터를 불러올 수 있는지 테스트
    show_external_data 파라미터를 true로 설정해 reco_hashkey 이외의 데이터도 나오는지 테스트

    input : 
        없음
    output : 
        저장된 모든 데이터

    assert 내용
        1. exptected output의 recohashkey가 output안에 들어있는가
        2. exptected output의 갯수와 output의 결과가 같은가

    """
    def test_load_all_external_2(self):
        print_test_info() 
        reco = Reco( 
            test_data['test_region_filter_1']['input'],
            show_external_data = False,
            external_data = {
                'item_data': test_item_data,
                'user_click': None
            }
        )
        recoList = reco.get_reco_list()
        expectedList = test_data['test_region_filter_1']['output']
        
        for category in expectedList:
            for row in recoList[category]:
                self.assertEqual(
                    1,
                    len(row)
                )

            for row in expectedList[category]:
                self.assertTrue(
                    row['reco_hashkey'] in [data['reco_hashkey'] for data in recoList[category]]
                )
            self.assertEqual(
                len(expectedList[category]),
                len(recoList[category])
            )

    """
    test_price_rank
    get_range()함수로 등급을 불러올때 올바르게 불러오는지 테스트

    input : 
        등급 기준표
        테스트할 가격 리스트
    output : 
        등급

    assert 내용
        1. exptected output의 등급과 output의 등급이 같은지 

    """
    def test_price_rank(self):
        print_test_info()
        reco = Reco(
            test_data['empty_data']['input'],
            True,
            external_data = {
                'item_data': test_item_data,
                'user_click': None
            }
        )
        array = test_data['test_price_rank']['input']['array']
        data = test_data['test_price_rank']['input']['data']
        expectedRank = test_data['test_price_rank']['output']['rank']

        for i in range(0, len(data)):
            rank = reco.get_range(array, data[i])
            self.assertEqual(
                rank,
                expectedRank[i]
            )


    """
    test_distance_rank
    get_range()함수로 등급을 불러올때 올바르게 불러오는지 테스트

    input : 
        등급 기준표
        테스트할 가격 리스트
    output : 
        등급

    assert 내용
        1. exptected output의 등급과 output의 등급이 같은지 

    """
    def test_distance_rank(self):
        print_test_info()
        reco = Reco(
            test_data['empty_data']['input'],
            True,
            external_data = {
                'item_data': test_item_data,
                'user_click': None
            }
        )
        array = test_data['test_distance_rank']['input']['array']
        data = test_data['test_distance_rank']['input']['data']
        expectedRank = test_data['test_distance_rank']['output']['rank']

        for i in range(0, len(data)):
            rank = reco.get_range(array, data[i])
            self.assertEqual(
                rank,
                expectedRank[i]
            )


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
            True,
            external_data = {
                'item_data': test_item_data,
                'user_click': None
            }
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
            True,
            external_data = {
                'item_data': test_item_data,
                'user_click': None
            }
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
            True,
            external_data = {
                'item_data': test_item_data,
                'user_click': None
            }
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
            True,
            external_data = {
                'item_data': test_item_data,
                'user_click': None
            }
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
            True,
            external_data = {
                'item_data': test_item_data,
                'user_click': None
            }
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
            True,
            external_data = {
                'item_data': test_item_data,
                'user_click': None
            }
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
            True,
            external_data = {
                'item_data': test_item_data,
                'user_click': None
            }
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

    """
    test_score_price_distance_1
    특정 지역목록을 넣고 score의 지역/거리점수가 공식에 맞게 계산되는지 테스트 

    input : 
        지역 : 신사역, 건대입구역  
    output : 
        신사역 목록 -> 백/십/일자리의수가 score 공식으로 계산된 지역/거리점수이어야함
        건대입구역 목록 -> 백/십/일자리의수가 score 공식으로 계산된 지역/거리점수이어야함

    assert 내용
        1. exptected output의 recohashkey가 output안에 들어있는가
        2. exptected output의 갯수와 output의 결과가 같은가
        3. output의 score의 백/십/일자리수와 expected output의 백/십/일자리수가 같은지

    """
    def test_score_price_distance_1(self):
        print_test_info()
        reco = Reco(
            test_data['test_score_price_distance_1']['input'],
            True,
            external_data = {
                'item_data': test_item_data,
                'user_click': None
            }
        )
        recoList = reco.get_reco_list()
        expectedList = test_data['test_score_price_distance_1']['output']

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
    test_score_personal_1
    특정 지역과 유저의 활동기록을 넣고 score의 개인화점수가 공식에 맞게 계산되는지 테스트 

    input : 
        지역 : 신사역, 건대입구역  
        유저활동기록(클릭수) : 
            전체 : 120
            한식 : 9
            중식 : 10
            일식 : 11
            양식 : 12
            로맨틱 : 40
            능동 : 18
            수동 : 22

    output : 
        신사역 목록 -> 천자리의수가 score 공식으로 계산된 목적점수이어야함
        건대입구역 목록 -> 천자리의수가 score 공식으로 계산된 목적점수이어야함

    assert 내용
        1. exptected output의 recohashkey가 output안에 들어있는가
        2. exptected output의 갯수와 output의 결과가 같은가
        3. output의 score의 천자리수와 expected output의 천자리수가 같은지

    """
    def test_score_personal_1(self):
        print_test_info()
        reco = Reco(
            test_data['test_score_personal_1']['input']['extracted_data'],
            True,
            external_data = {
                'item_data': test_item_data,
                'user_click': test_data['test_score_personal_1']['input']['user_click']
            }
        )
        recoList = reco.get_reco_list()
        expectedList = test_data['test_score_personal_1']['output']

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
    test_score_personal_2
    특정 지역과 유저의 활동기록을 넣고 score의 개인화점수가 공식에 맞게 계산되는지 테스트 

    input : 
        지역 : 신사역, 건대입구역  
        유저활동기록(클릭수) : 
            전체 : 10
            한식 : 3
            중식 : 0
            일식 : 0
            양식 : 0
            로맨틱 : 9
            능동 : 1
            수동 : 0

    output : 
        신사역 목록 -> 천자리의수가 score 공식으로 계산된 목적점수이어야함
        건대입구역 목록 -> 천자리의수가 score 공식으로 계산된 목적점수이어야함

    assert 내용
        1. exptected output의 recohashkey가 output안에 들어있는가
        2. exptected output의 갯수와 output의 결과가 같은가
        3. output의 score의 천자리수와 expected output의 천자리수가 같은지

    """
    def test_score_personal_2(self):
        print_test_info()
        reco = Reco(
            test_data['test_score_personal_2']['input']['extracted_data'],
            True,
            external_data = {
                'item_data': test_item_data,
                'user_click': test_data['test_score_personal_2']['input']['user_click']
            }
        )
        recoList = reco.get_reco_list()
        expectedList = test_data['test_score_personal_2']['output']

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
    test_score_personal_3
    특정 지역과 유저의 활동기록을 넣고 score의 개인화점수가 공식에 맞게 계산되는지 테스트 

    input : 
        지역 : 신사역, 건대입구역  
        유저활동기록(클릭수) : 
            전체 : 50
            한식 : 3
            중식 : 3
            일식 : 3
            양식 : 3
            로맨틱 : 20
            능동 : 10
            수동 : 10

    output : 
        신사역 목록 -> 천자리의수가 score 공식으로 계산된 목적점수이어야함
        건대입구역 목록 -> 천자리의수가 score 공식으로 계산된 목적점수이어야함

    assert 내용
        1. exptected output의 recohashkey가 output안에 들어있는가
        2. exptected output의 갯수와 output의 결과가 같은가
        3. output의 score의 천자리수와 expected output의 천자리수가 같은지

    """
    def test_score_personal_3(self):
        print_test_info()
        reco = Reco(
            test_data['test_score_personal_3']['input']['extracted_data'],
            True,
            external_data = {
                'item_data': test_item_data,
                'user_click': test_data['test_score_personal_3']['input']['user_click']
            }
        )
        recoList = reco.get_reco_list()
        expectedList = test_data['test_score_personal_3']['output']

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
    
    


# 테스트 실행
if __name__ == '__main__':
	unittest.main(argv=[sys.argv[0]])
#    test = TestReco("test_score_personal_3")
#    test.test_score_personal_3()
