
#####
##TODO 
##1. 주변역찾아서 두번째 value로 값넣어주기.
##2. 다양한 testcase찾아보기.
##3. 성민이한테 텀겨줄데이터 세팅하기.
##4. 완성된데이터 db에 넣기.
import datetime

from reinforce.common import db_manager
from reinforce.common.util import utils
from enum import Enum

reinforce_result = lambda state,data : {'code':state,'event_info_data':data}

class EventRecoStatusCode(Enum):

	#모든 데이터가 잘들어가있는경우. => 바로 리턴. 
	RECO_PERFECT = 1	

	#비추천일 경우.  => 
	#1.이벤트타입이 없어서. 
	#2.아예 비추천 항목일경우.		
	RECO_CANT = 2

	#추천불가이긴한데. 사유가 우리가 지원하지 않는 로케이션이여서이다.
	RECO_CANT_IMPOSSIBLE_LOCA = 3

	#위치가없고 이벤트타입이 있는경우.
	RECO_NO_LOCA_HAS_EVENTTYPE = 4


	#현재 두개다 타입이 없어서 비추천 일 경우이다.
	RECO_NO_LCOA_NO_EVENTTYPE = 5

	#위치는 존재하고 이벤트 타입이 없을경우 추천해주기로한다. 대신 none으로 그대로넘긴다.
	RECO_HAS_LOCA_NO_EVENTTYPE = 6



class Reinforce:

	def __init__(self,event_info_data):
		self.__event_reco_status_code = EventRecoStatusCode.RECO_CANT 
		self.event_info_data = event_info_data	
		self.event_reco_result = reinforce_result(EventRecoStatusCode.RECO_CANT.value,self.event_info_data)							
		#형태소 분석기에서 나온 상태가 현재 어떤 추천 상태를 가질수 있는지를 판단합니다.
		self.__check_reco_stauts()
		#위에서 정해진 상태를보고 어떻게 이벤트데이터를 추천할지 정해 추천해줍니다.
		self.__rein_force_for_eventData()
		#추천된 장소가 실제 추천 가능한지 판단해 줍니다. 
		# self.__check_is_reco_possible_loca()


	

	def __check_reco_stauts(self):
		#모든데이터가 잘들어가 있는경우
		if self.event_info_data["locations"] != None and self.event_info_data["locations"] != "Cannot"  and self.event_info_data["event_types"] != None:
			self.__event_reco_status_code = EventRecoStatusCode.RECO_PERFECT  

		#location이 cannot일경우 데이터를 추천해 줄 수없다. 아예 비추천.		
		elif self.event_info_data["locations"] == "Cannot" :		
			self.__event_reco_status_code = EventRecoStatusCode.RECO_CANT  

		#eventType이 None일경우 데이터를 추천해 줄 수 없다.	
		elif  self.event_info_data["event_types"] == None:
			# 목적이 없고, 장소도 없는경우
			if self.event_info_data["locations"] == None:
				self.__event_reco_status_code = EventRecoStatusCode.RECO_NO_LCOA_NO_EVENTTYPE
			#이벤트가 있는경우.
			else:
				self.__event_reco_status_code = EventRecoStatusCode.RECO_HAS_LOCA_NO_EVENTTYPE				

		#위치가없고 이벤트타입이 있는경우.
		elif self.event_info_data["locations"] == None and self.event_info_data["event_types"] != None:						
			self.__event_reco_status_code = EventRecoStatusCode.RECO_NO_LOCA_HAS_EVENTTYPE




	def __get_possible_loca_In_db(self,locaMainSubway):
		return	utils.fetch_all_json(
					db_manager.query(
							"""
							SELECT region FROM RECOMMENDATION 
							WHERE region = %s
							""",			
							(locaMainSubway,)				
					)
				)
			
	# def __check_support_region(self,region,locations):
	# 	rows = self.__get_possible_loca_In_db(region)
	# 	#로케이션이 수원같은경우면 더이상 주위역을 찾을 필요가없다. => 비추천.
	# 	if len(rows) == 0 :
	# 		#!!!RECOMMENDATION
	# 		self.event_reco_result = reinforce_result(EventRecoStatusCode.RECO_CANT_IMPOSSIBLE_LOCA.value,None)							
	# 	#실제 정책상 지원해줄수 있는경우이다.
	# 	else:	
	# 		surrounding_station =  self.__set_surrounding_station(region)				
	# 		if surrounding_station != None:
	# 			locations.append({
	# 					"no" : 1,
	# 					"region" : surrounding_station
	# 				})		

	def __rein_force_for_eventData(self):

		# 추천이 완벽할경우.값을 바로 사용할수있도록 한다.
		if self.__event_reco_status_code == EventRecoStatusCode.RECO_PERFECT:
			
			locations = self.event_info_data["locations"]
			#locations의 길이가 1이라면..
			if len(locations) == 1:
				region = locations[0]["region"]

				rows = self.__get_possible_loca_In_db(region)
				#로케이션이 수원같은경우면 더이상 주위역을 찾을 필요가없다. => 비추천.
				if len(rows) == 0 :
					#!!!RECOMMENDATION
					self.event_reco_result = reinforce_result(EventRecoStatusCode.RECO_CANT_IMPOSSIBLE_LOCA.value,None)							
				#실제 정책상 지원해줄수 있는경우이다.
				else:	
					surrounding_station =  self.__set_surrounding_station(region)				
					if surrounding_station != None:
						locations.append({
								"no" : 1,
								"region" : surrounding_station
							})

					self.event_reco_result = reinforce_result(self.__event_reco_status_code.value,self.event_info_data)							

			#db에 최종본 저장
			
			self.__set_event_analaysisDB()
			self.__set_user_hashkey_in_result()

		elif self.__event_reco_status_code == EventRecoStatusCode.RECO_CANT or self.__event_reco_status_code == EventRecoStatusCode.RECO_NO_LCOA_NO_EVENTTYPE :
			#db에 최종본 저장
			self.__set_event_analaysisDB()
			
			#현재infojson을 사용할수없게 값을 리턴해줍니다.
			self.event_reco_result = reinforce_result(self.__event_reco_status_code.value,None)

			#로케이션은 있는데 이벤트가 없는 경우.
		elif self.__event_reco_status_code == EventRecoStatusCode.RECO_HAS_LOCA_NO_EVENTTYPE:

			locations = self.event_info_data["locations"]
			#locations의 길이가 1이라면..
			if len(locations) == 1:
				region = locations[0]["region"]

				rows = self.__get_possible_loca_In_db(region)
				#로케이션이 수원같은경우면 더이상 주위역을 찾을 필요가없다. => 비추천.
				if len(rows) == 0 :
					#!!!RECOMMENDATION
					self.event_reco_result = reinforce_result(EventRecoStatusCode.RECO_CANT_IMPOSSIBLE_LOCA.value,None)							
				#실제 정책상 지원해줄수 있는경우이다.
				else:	
					surrounding_station =  self.__set_surrounding_station(region)				
					if surrounding_station != None:
						locations.append({
								"no" : 1,
								"region" : surrounding_station
							})

					self.event_reco_result = reinforce_result(self.__event_reco_status_code.value,self.event_info_data)		


			self.__set_event_analaysisDB()
			self.__set_user_hashkey_in_result()
			# self.event_reco_result = reinforce_result(self.__event_reco_status_code.value,self.event_info_data)
			
		#이벤트 타입이 있는데, 로케이션이 없다면, 
		#1. 유저 DB에서 가져와야 한다. 
		#2. 핫플레이스에서 가져와야한다. 		
		elif self.__event_reco_status_code == EventRecoStatusCode.RECO_NO_LOCA_HAS_EVENTTYPE:		
			#유저DB에 가져온경우나, hotplace인 경우는 유저 실제데이터가 아님으로 location에 저장하지 않아야함으로 바로 현재데이터를 db에 저장한다.			
			self.__set_event_analaysisDB()

			rows = utils.fetch_all_json(
					db_manager.query(
							"""
							SELECT region, count(*) as locationCnt FROM
							(
							SELECT ul.region,ul.location_hashkey,ul.priority 
							FROM EVENT e, USER_EVENT_ANALYSIS ue , USER_EVENT_LOCATION ul ,
							(
							# 여기까지 유저 accounthashkey가 같은 calendar 가져오기
							SELECT calendar_hashkey FROM CALENDAR
							INNER JOIN(
							#여기까지 이벤트 해시키로 유저 account_hashkey들 가져오는쿼리
							SELECT account_hashkey FROM USERACCOUNT
							WHERE user_hashkey IN (
							SELECT user_hashkey 
							FROM EVENT e, CALENDAR c, USERACCOUNT u
							WHERE e.event_hashkey = %s
							AND c.calendar_hashkey = e.calendar_hashkey
							AND u.account_hashkey = c.account_hashkey
							)	
							#############
							) AS u
							ON u.account_hashkey = CALENDAR.account_hashkey
							#############
							) cal
							WHERE e.calendar_hashkey = cal.calendar_hashkey
							AND ue.event_hashkey = e.event_hashkey
							AND ue.location_hashkey = ul.location_hashkey
							AND ul.priority = 0
							) AS locations
							GROUP by region
							ORDER BY locationCnt DESC , region ASC
							""",
							(self.event_info_data["event_hashkey"],)
					)
			)
			new_locations = []
			#유저데이터가 있을경.
			if len(rows) != 0:
				region = rows[0]["region"]	
				noRecoRows = self.__get_possible_loca_In_db(region)
				#로케이션이 수원같은경우면 핫플레이스를 검색해 보여
				if len(noRecoRows) == 0 :
					self.__set_hot_place(new_locations)
					self.event_reco_result = reinforce_result(self.__event_reco_status_code.value,self.event_info_data)
					# self.event_reco_result = reinforce_result(EventRecoStatusCode.RECO_CANT_IMPOSSIBLE_LOCA.value,None)							
				else:
					new_locations.append({
							"no" : 0,
							"region" : rows[0]["region"]
						})				
					surrounding_station =  self.__set_surrounding_station(region)				
					if surrounding_station != None:				
						new_locations.append({
								"no" : 1,
								"region" : surrounding_station
							})
						self.event_reco_result = reinforce_result(self.__event_reco_status_code.value,self.event_info_data)
				

			#유저데이터가 없을때
			#hotplace를 넣어준다.
			else:
				self.__set_hot_place(new_locations)

			self.event_info_data["locations"] = new_locations	

			
			self.__set_user_hashkey_in_result()
			
	def __set_hot_place(self,new_locations):
		rows = utils.fetch_all_json(
			
			db_manager.query(
					"""
					SELECT * FROM DEFAULT_HOT_PLACE ORDER BY id DESC LIMIT 2
					""",							
			)
			# db_manager.query(
			# 		"""
			# 		SELECT * FROM
			# 		(SELECT * FROM DEFAULT_HOT_PLACE ORDER BY rand() LIMIT 2 ) AS e
			# 		ORDER BY id
			# 		""",							
			# )					
		)

		for idx,row in enumerate(rows):	
			new_locations.append({
					"no" : idx ,
					"region" : row["region"]
			})				
	
		self.event_reco_result = reinforce_result(self.__event_reco_status_code.value,self.event_info_data)		

	def __set_surrounding_station(self,station_name):	
		rows = utils.fetch_all_json(
				db_manager.query(
						"""
					SELECT surrounding_station FROM SUBWAY_INFO
					WHERE station_name = %s and address LIKE '서울특별%'
					limit 1
						""",
						(station_name[:len(station_name)-1],)
				)
		)		
		if len(rows) == 0:
			return None
		else:
			return rows[0]["surrounding_station"] + "역"	

	def __set_user_hashkey_in_result(self):
		rows = utils.fetch_all_json(
			db_manager.query(
					"""
					SELECT user_hashkey FROM USERACCOUNT
					WHERE user_hashkey IN(
					SELECT user_hashkey 
					FROM EVENT e, CALENDAR c, USERACCOUNT u
					WHERE e.event_hashkey = %s
					AND c.calendar_hashkey = e.calendar_hashkey
					AND u.account_hashkey = c.account_hashkey
					) ORDER BY user_hashkey LIMIT 1
					""",					
					(self.event_info_data["event_hashkey"],)		
			)
		)	
		user_hashkey = rows[0]["user_hashkey"]	
		self.event_info_data["user_hashkey"]= user_hashkey



	def __set_event_analaysisDB(self):
		locations = self.event_info_data["locations"]
		#locations db에 다 넣어줌.
		event_hashkey = self.event_info_data["event_hashkey"]
		rows = utils.fetch_all_json(
			db_manager.query(
					"""
					SELECT *FROM USER_EVENT_ANALYSIS
					WHERE event_hashkey = %s					
					""",		
					(self.event_info_data["event_hashkey"],)					
			)
		)
		print("userAnalysis = > "+ str(rows))
		if len(rows) == 0:
				
			#로케이션이 None이아니면
			if locations == None or locations == "Cannot":
				location_hashkey = None
			#로케이션이 None이면
			#로케이션 해시키가 Null이다.
			else:

				location_hashkey = utils.make_hashkey(event_hashkey)
				for location in locations:
					db_manager.query(
							"""
							INSERT INTO USER_EVENT_LOCATION
							(location_hashkey,priority,region)
							VALUES (%s,%s,%s)
							""",		
							(location_hashkey,location["no"],location["region"])					
					)



			#type 넣어줌
			
			event_types = self.event_info_data["event_types"]
			#이벤트 타입이 존재하면
			if event_types == None:
				type_hashkey = None
				
			#event Type이 None이면
			#type hashkey가 null이다.
			else :
				type_hashkey = utils.make_hashkey(event_hashkey)
				for event_type in event_types:
					db_manager.query(
							"""
							INSERT INTO USER_EVENT_TYPE
							(type_hashkey,event_type)
							VALUES (%s,%s)
							""",		
							(type_hashkey,event_type["id"])					
					)			

			#유저시간에맞도록 디비에 넣어준
			rows = utils.fetch_all_json(
				db_manager.query(
						"""
						SELECT *FROM EVENT
						WHERE event_hashkey = %s
						""",		
						(self.event_info_data["event_hashkey"],)					
				)
			)

			event = rows[0]
			
			startEventDate = datetime.datetime.strptime(event["start_dt"], '%Y-%m-%d %H:%M:%S')
			endEventDate = datetime.datetime.strptime(event["end_dt"], '%Y-%m-%d %H:%M:%S')

			event_start_date = str(startEventDate.year) + "-" + str(startEventDate.month) + "-" + str(startEventDate.day)
			event_end_date =  str(endEventDate.year) + "-" + str(endEventDate.month) + "-" + str(endEventDate.day)

			extract_start = self.event_info_data["time_set"]["extract_start"]
			extract_end = self.event_info_data["time_set"]["extract_end"]
			event_start = self.event_info_data["time_set"]["event_start"]
			event_end = self.event_info_data["time_set"]["event_end"]

			if extract_start != None:
				extract_start = event_start_date + " " + extract_start
				extract_end = event_end_date + " " + extract_end
			else :
				extract_start = None
				extract_end = None

			event_start = event_start_date + " " + event_start
			event_end = event_end_date + " " + event_end

			db_manager.query(
						"""
						INSERT INTO USER_EVENT_ANALYSIS
						(event_hashkey,location_hashkey,extract_start,extract_end,event_start,event_end,type_hashkey)
						VALUES (%s,%s,%s,%s,%s,%s,%s)
						""",		
						(event_hashkey,location_hashkey,extract_start,extract_end,event_start,event_end,type_hashkey)					
				)

				