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
            item_data = test_item_data
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
            '',
            item_data = test_item_data
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
            '',
            item_data = test_item_data
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
            '',
            item_data = test_item_data
        )
        recoList = reco.get_reco_list()
        expectedList = test_data['test_score_price_distance_1']['output']

        for category in expectedList:
            for row in expectedList[category]:
                print(row)
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
                print(row['score'])
                print(recoItem['score'])
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
    TODO
    test_score_personal_1
    특정 지역을 넣고 score의 개인화점수가 공식에 맞게 계산되는지 테스트 

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
    def test_score_personal_1(self):

        self.assertTrue(True)
    

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