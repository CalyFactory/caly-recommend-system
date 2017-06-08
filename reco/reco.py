from common import db_manager
from common.util import utils
from common import mongo_manager
import json
import re
import random
import math
from bson.json_util import dumps


class Reco:

    price_priority = {
        'restaurant':67.3, 
        'cafe':41.1, 
        'place':57.4
    }
    distance_priority = {
        'restaurant':30.1, 
        'cafe':36.55, 
        'place':40.7
    }

    def __init__(self, json_data, show_external_data = True, item_data = None):
        self.json_data = json_data
        if 'user_hashkey' not in json_data:
            self.user_hashkey = ''
        else:
            self.user_hashkey = json_data['user_hashkey']
        self.show_external_data = show_external_data
        self.item_data = item_data

        self.init_data()

    def init_data(self):
        self.location_priority_list = {}
        for location_data in self.json_data['locations']:
            self.location_priority_list[location_data['region']] = location_data['no']

        self.event_type_id_list = []
        for event_type in self.json_data['event_types']:
            self.event_type_id_list.append(event_type['id'])
        
        price_list = utils.fetch_all_json(
            db_manager.query(
                """
                SELECT price 
                FROM RECOMMENDATION
                WHERE price IS NOT NULL
                ORDER BY price 
                """
            )
        )

        distance_row_list = utils.fetch_all_json(
            db_manager.query(
                """
                SELECT distance 
                FROM RECOMMENDATION
                WHERE distance IS NOT NULL
                ORDER BY distance 
                """
            )
        )

        distance_list = []
        for distance_row in distance_row_list:
            distance_string = re.search(r'\d+', distance_row['distance'])
            if distance_string is None:
                distance_data = 99
            else:
                distance_data = int(distance_string.group())
            distance_list.append(distance_data)

        distance_list.sort()

        self.price_grade_list = []
        self.distance_grade_list = []

        n = 9

        for i in range(1, n + 1):
            position = int(self.get_snd_percent(n, i) * len(price_list)) - 1
            self.price_grade_list.append(price_list[position]['price'])

            position = int(self.get_snd_percent(n, i) * len(distance_list)) - 1
            self.distance_grade_list.append(distance_list[position])
            #print(self.get_snd_percent(n, i))
        #print(self.price_grade_list)
        #print(self.distance_grade_list)

        result = utils.fetch_all_json(
            db_manager.query(
                """
                SELECT account_hashkey
                FROM USERACCOUNT
                WHERE
                user_hashkey = '%s'
                """
                % self.user_hashkey
            )
        )
        account_hash_key_list = []
        for row in result:
            account_hash_key_list.append(row['account_hashkey'])

        #load user data 
        reco_log_list = json.loads(
            dumps(
                mongo_manager.reco_log.find(
                    {
                        "accountHashkey": {
                            "$all": account_hash_key_list
                        }
                    }
                )
            )
        )
        #print(account_hash_key_list)
        #print(reco_log_list)

        
        log_leco_hashkey_list = []
        for reco_log in reco_log_list:
            if (reco_log['action'] == "click" and reco_log['category'] == "recoCell" and reco_log['label'] == "deepLink") or \
                (reco_log['action'] == "click" and reco_log['category'] == "recoCell" and reco_log['label'] == "sharingKakao") or \
                (reco_log['action'] == "click" and reco_log['category'] == "recoCell" and reco_log['label'] == "sharingKakaoInBlog") or \
                (reco_log['action'] == "click" and reco_log['category'] == "recoMapCell" and reco_log['label'] == "deepLink") or \
                (reco_log['action'] == "click" and reco_log['category'] == "recoMapCell" and reco_log['label'] == "sharingKakaoInCell"):
                log_leco_hashkey_list.append(reco_log['recoHashkey'])
        
        if len(log_leco_hashkey_list) != 0:
            result = utils.fetch_all_json(
                db_manager.query(
                    """
                    SELECT 
                        reco_hashkey,
                        property_romantic, 
                        property_active_dynamic, 
                        property_active_static, 
                        property_food_korean, 
                        property_food_chinese, 
                        property_food_japanese, 
                        property_food_italian
                    FROM RECOMMENDATION
                    WHERE 
                    RECOMMENDATION.reco_hashkey IN (%s)
                    """ %
                    (
                        ", ".join("'%s'" % row for row in log_leco_hashkey_list)
                    )
                )
            )
        else:
            result = []
        
        self.user_type_click_count = {
            'property_romantic':0,
            'property_active_dynamic':0,
            'property_active_static':0,
            'property_food_korean':0,
            'property_food_chinese':0,
            'property_food_japanese':0,
            'property_food_italian':0,
            'all':len(log_leco_hashkey_list)
        }
        
        for row in result:
            hashkey_num = log_leco_hashkey_list.count(row['reco_hashkey'])
            for key in row:
                if row[key] == None:
                    continue
                if key == 'reco_hashkey':
                    continue
                self.user_type_click_count[key] += row[key] * hashkey_num
        #print(self.user_type_click_count)
        self.user_property_score = {}
        if self.user_type_click_count['all'] == 0:
            self.user_property_score['romanticPriority'] = 0.5
        else:
            self.user_property_score['romanticPriority'] = (
                self.user_type_click_count['property_romantic'] / self.user_type_click_count['all']
            )
        active_list = [
            'property_active_dynamic',
            'property_active_static'
        ]
        food_list = [
            'property_food_korean',
            'property_food_chinese',
            'property_food_japanese',
            'property_food_italian'
        ]
        food_list.sort(
            key = lambda e:(self.user_type_click_count[e]),
            reverse = True
        )
        active_list.sort(
            key = lambda e:(self.user_type_click_count[e]),
            reverse = True
        )
        
        i = 0
        for active_row in active_list:
            self.user_property_score[active_row] = 4.5 - i
            i+=1
            
        i = 0
        for food_row in food_list:
            self.user_property_score[food_row] = 4.5 - i
            i+=1
        #print(self.user_property_score)

    def get_snd_percent(self, n, index):
        if n == index:
            return 1
        point = (index - n / 2) / 2
        score = self.__get_snd_score(point)
        return score
    
    def __get_snd_score(self, x):
        return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

    def get_reco_list(self):
        filtered_list = self.get_filtered_list()
        #allList = self.get_all_list()
        sorted_list = self.sort_list_by_score(filtered_list)

        #카테고리별로 분류해서 리턴하기
        return sorted_list

    def get_all_list(self):

        reco_list = self.__get_all_list()

        return reco_list

    def get_filtered_list(self):

        location_filtered_list = self.__get_location_filtered_list()
#        timeFilteredList = self.__get_time_filtered_list(location_filtered_list)
#        typeFilteredList = self.__get_type_filtered_list(location_filtered_list)

        return location_filtered_list

    #두 객체의 우선순위 비교하는 함수
    #첫 번째 인자의 우선순위가 높을경우 True, 아닐경우 False 를 리턴함
    def is_second_arg_high_priority(self, item_a, item_b):

        if item_a['score'] < item_b['score']:
            return True 
        else:
            return False 

        #region
        item_a_region_priority = self.location_priority_list[item_a['region']]
        item_b_region_priority = self.location_priority_list[itemB['region']]

        if item_a_region_priority < item_b_region_priority:
            return False
        elif item_a_region_priority > item_b_region_priority:
            return True

        #목적지표 event_type_availability
        ## TODO : 회의때 목적은 여러개인데 목적지표로 순위를 정하는것을 목적이 하나인 경우만 생각해서 정한 것 같다. 고민이 필요함

        event_type_id = self.json_data['event_types'][0]['id']

        item_a_availability_score = self.__get_availability_score(is_second_arg_high_priority, event_type_id)
        item_b_availability_score = self.__get_availability_score(item_b, event_type_id)

        if item_a_availability_score > item_b_availability_score:
            return False 
        elif item_a_availability_score < item_b_availability_score:
            return True 

        #score 
        item_a_score = is_second_arg_high_priority['score']
        item_b_score = item_b['score']

        if item_a_score < item_b_score:
            return False 
        elif item_a_score > item_b_score:
            return True 

        #등록된 시간 순서대로

        return True

        

    def __get_availability_score(self, item, event_type_id):

        #TODO : 테스트중이라 주석차리 하지만 event_type_id가 없는경우가 존재해서는 안됨. 실제론 error를 내야함 
        if event_type_id not in item['event_availability']:
            #raise Exception('no event_type_id in item')
            return 0 # 테스트 후 raise문을 사용할것
        
        ing_value = item['event_availability'][event_type_id]['ing'] 

        return ing_value * 2 + afterValue

    def sort_list_by_score(self, origin_list):

        """
        랭킹 순위
        1. 장소
        2. 목적지표
        3. score (가격 + 거리)
        
        """

        #score 계산
        for row in origin_list:
            for origin_data in origin_list[row]:
                origin_data['score'] = self.__getScore(origin_data)
                
        #정렬 
        for row in origin_list:
            for i in range(0, len(origin_list[row])):
                for j in range(i, len(origin_list[row])):
                    if self.is_second_arg_high_priority(origin_list[row][i], origin_list[row][j]):
                        tmp = origin_list[row][i]
                        origin_list[row][i] = origin_list[row][j]
                        origin_list[row][j] = tmp
            for i in range(0, len(origin_list[row])):
                origin_list[row][i]['no'] = i
               
        """
        #필터링 
        
        for row in origin_list:
            for origin_data in origin_list[row][:]:      
                if origin_data['score'] < 10000:
                    origin_list[row].remove(origin_data)
        """
        if self.show_external_data == False:
            origin_list = self.extract_only_reco_hashkey(origin_list)
        return origin_list
    
    def extract_only_reco_hashkey(self, origin_list):
        reco_list = {}
        for row in origin_list:
            reco_list[row] = []
            for origin_data in origin_list[row]:
                reco_list[row].append(
                    origin_data['reco_hashkey']
                )
        return reco_list

    def get_range(self, array, value):
        for i in range(0, len(array)):
            if value<=array[i]:
                return i + 1
        return len(array)

    def __getScore(self, origin_data):

        score = 0

        #region 
        if origin_data['region'] in self.location_priority_list:
            score += (9 - self.location_priority_list[origin_data['region']]) * 100000

        #목적

        for i in range(0, len(self.event_type_id_list)):
            event_type_id = self.event_type_id_list[i]
            ing_value = 1
            if event_type_id in origin_data['event_availability']:
                ing_value = origin_data['event_availability'][event_type_id]['ing']
            # ○ => 3   //*2000
            # △ => 2  //*1000
            # × => 1   //*0

            score += ((ing_value - 1) * 10000) 
      
        # 개인화 점수 

        personal_score = 0

        property_list = [
            'property_romantic',
            'property_active_dynamic',
            'property_active_static',
            'property_food_korean',
            'property_food_chinese',
            'property_food_japanese',
            'property_food_italian',
        ]
        for property_row in property_list:
            if origin_data[property_row] == None:
                origin_data[property_row] = 0
            if property_row == 'property_romantic':
                if self.user_property_score['romanticPriority'] > 0.5:
                    personal_score += origin_data['property_romantic'] * 4.5
                else:
                    personal_score += (1 - origin_data['property_romantic']) * 4.5
            else:
                personal_score += origin_data[property_row] * self.user_property_score[property_row]

        """
        print(personal_score)
        print(
            "title : %s \nromantic : %s\n dynamic : %s\n static : %s\n korean : %s\n chinese : %s\njapanese : %s \nitalian : %s\n\n" 
            %
            (
                origin_data['title'],
                origin_data['property_romantic'],
                origin_data['property_active_dynamic'],
                origin_data['property_active_static'],
                origin_data['property_food_korean'],
                origin_data['property_food_chinese'],
                origin_data['property_food_japanese'],
                origin_data['property_food_italian']
            ) 
        )
        print("==")
        """
        score += int(personal_score) * 1000
        
        #가격

        price_data = origin_data['price']
        distance_string = re.search(r'\d+', origin_data['distance'])
        if distance_string is None:
            distance_data = 99
        else:
            distance_data = int(distance_string.group())
        
        price_rank = self.get_range(self.price_grade_list, price_data)
        distance_rank = self.get_range(self.distance_grade_list, distance_data)

        sum_priority = self.price_priority[origin_data['category']] + self.distance_priority[origin_data['category']]
        price_priority = self.price_priority[origin_data['category']] / sum_priority
        distance_priority = self.distance_priority[origin_data['category']] / sum_priority

        score += int(10 - (price_rank * price_priority + distance_rank * distance_priority) * 100)



        return score

    def __get_all_list(self):
        if self.item_data != None:
            recoList = {}

            for row in self.item_data:
                recoList[row] = []
                for item in self.item_data[row]:
                    recoList[row].append(item)

            return recoList
        data_list = utils.fetch_all_json(    
            db_manager.query(
                """
                SELECT 
                    r.reco_hashkey, 
                    r.region, 
                    r.title,
                    r.price, 
                    r.distance,
                    r.category,
                    r.property_romantic,
                    r.property_active_dynamic,
                    r.property_active_static,
                    r.property_food_korean,
                    r.property_food_chinese,
                    r.property_food_japanese,
                    r.property_food_italian,
                    CONCAT(
                        "[",
                        GROUP_CONCAT(
                            JSON_OBJECT(
                                'id', etr.id,
                                'event_type_id', etr.event_type_id,
                                'ing', etr.ing
                            )
                        ),
                        "]"
                    ) as event_availability 
                FROM RECOMMENDATION as r
                LEFT JOIN EVENT_TYPE_RECO as etr
                ON
                    r.reco_hashkey = etr.reco_hashkey
                GROUP BY r.reco_hashkey
                """
            )
        )

        reco_list = {
            'restaurant': [],
            'cafe': [],
            'place': []
        }

        for data_item in data_list:
            reco_list[data_item['category']].append(data_item)
        
        for data_item in reco_list:
        
            for reco_item in reco_list[data_item]:
                json_converted_item = json.loads(reco_item['event_availability'])
                reco_item['event_availability'] = {}
                for json_item in json_converted_item:
                    if json_item['event_type_id'] == None:
                        continue
                    reco_item['event_availability'][json_item['event_type_id']] = json_item
        
        return reco_list

        
    def __get_location_filtered_list(self):
        location_list = self.json_data['locations']
        if self.item_data != None:
            recoList = {}
            location_data = [row['region'] for row in location_list]
            for row in self.item_data:
                recoList[row] = []
                for item in self.item_data[row]:
                    if item['region'] in location_data:
                        recoList[row].append(item)

            return recoList
        
        query_option_param = ", ".join("'%s'" % location_data['region'] for location_data in location_list)

        data_list = utils.fetch_all_json(
            db_manager.query(
                """
                SELECT 
                    r.reco_hashkey, 
                    r.region, 
                    r.title,
                    r.price, 
                    r.distance,
                    r.category,
                    r.property_romantic,
                    r.property_active_dynamic,
                    r.property_active_static,
                    r.property_food_korean,
                    r.property_food_chinese,
                    r.property_food_japanese,
                    r.property_food_italian,
                    CONCAT(
                        "[",
                        GROUP_CONCAT(
                            JSON_OBJECT(
                                'id', etr.id,
                                'event_type_id', etr.event_type_id,
                                'ing', etr.ing
                            )
                        ),
                        "]"
                    ) as event_availability 
                FROM RECOMMENDATION as r
                LEFT JOIN EVENT_TYPE_RECO as etr
                ON
                    r.reco_hashkey = etr.reco_hashkey
                WHERE
                    region IN (%s)
                GROUP BY r.reco_hashkey
                """ %
                query_option_param
            )
        )

        reco_list = {
            'restaurant': [],
            'cafe': [],
            'place': []
        }

        for data_item in data_list:
            reco_list[data_item['category']].append(data_item)
        
        for data_item in reco_list:
        
            for reco_item in reco_list[data_item]:
                json_converted_item = json.loads(reco_item['event_availability'])
                reco_item['event_availability'] = {}
                for json_item in json_converted_item:
                    if json_item['event_type_id'] == None:
                        continue
                    reco_item['event_availability'][json_item['event_type_id']] = json_item
        
        return reco_list

    def __get_time_filtered_list(self, origin_list):
        timeData = self.json_data['time']
        return origin_list 

    def __get_type_filtered_list(self, origin_list):
        event_type_data = self.json_data['event_types']
        event_type_id = self.json_data['event_types'][0]['id']

        for row in origin_list:
            for origin_data in origin_list[row][:]:            
                if event_type_id not in origin_data['event_availability']: 
                    #raise Exception('no event_type_id in item') #TODO : 테스트일때만 에러를 생략
                    ing = 0
                else:
                    ing = origin_data['event_availability'][event_type_id]['ing']

    #            if ing + after == 0: #TODO : 테스트 일때만 필터링을 안함
    #                origin_list.remove(origin_data)
        return origin_list

def hello():
    result = utils.fetch_all_json(
        db_manager.query(
            """
            SELECT * FROM USER ACCOUNT 
            WHERE is_active = %s
            """,
            (1,)
        )
    )

