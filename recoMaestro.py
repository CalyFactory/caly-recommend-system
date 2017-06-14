
from common import db_manager
from common.util import utils
from extractor.event_extractor import extract_info_from_event
from reinforce.reinforce import Reinforce


class RecoMaestro():	

	
	def __init__(self, account_hashkey = None, switchExtractor = False):
		#유저 계정해시키를 저장한다.
		self.account_hashkey = account_hashkey

		self.calendar_hashkey = None
		self.calendar_name = None
		self.user_event_hashkey = None
		#실제 유저 이벤트
		self.result_events = []
		#[웹뷰용]형태소분석 된 이후 분석된 이벤트 정보를 웹뷰에 보여주기위한 데이터
		self.result_analysis_events_for_web = []
		#최종 웹에 보여줄 데이터
		self.result_final= {}
		#[웹뷰용]보강된 데이터 넘겨줄 배열
		self.result_reinforce_events_for_web = []
		#실제 넘길데이터
		self.result_reinforce_events_real = []

		self.event = {}
		self.reinforce_json = {}
		self.fextracted_json = {}
		self.serMainRegion = {}		

		self.result_statis_json = {}


		self.statis_reco_perfect_cnt = 0
		self.statis_reco_cant_cnt = 0
		self.statis_reco_no_loca_has_evnttype = 0
		self.statis_reco_no_loca_no_evnttype = 0
		self.statis_reco_has_loca_no_evnttype = 0

		self.statis_recommended_cnt = 0
		self.statis_no_recommended_cnt = 0

		self.switchExtractor = switchExtractor

		
		self.main()
	


	def __get__(self, obj, objtype):
		return self.val

	def __set__(self, obj, val):
		self.val = val

	



	def main(self):
		#calendarlist를 추출한다.
		calendars  = self.__getCalendarList(self.account_hashkey)
		for calendar in calendars:
			self.calendar_hashkey = calendar["calendar_hashkey"]
			self.calendar_name = calendar["calendar_name"]
			events = self.__getEventsList(self.calendar_hashkey)
			
			for event in events:
				if 'summary' in event:
					print("events ==>" + str(event))
					self.event = event

					self.__appendEvent()				

					self.__extractFromEvent()

					print("extcted_json => "+ str(self.extracted_json))
					self.__append_analaysis_events_for_web()

					self.__checkRecoStauts()
		
		
		self.__getUserMainRegion()		
		self.__makeFinalReuslt()


	def __getUserMainRegion(self):
		self.userMainRegion = utils.fetch_all_json(
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
								ORDER BY locationCnt DESC
								LIMIT 3				
					""",							
					(self.user_event_hashkey,)
				)
			)		

	def __makeFinalReuslt(self):
		self.result_final["originEvents"] = self.result_events
		self.result_final["analysisEvents"] = self.result_analysis_events_for_web
		self.result_final["reinforceEvents"] = self.result_reinforce_events_for_web
		self.result_final["reinforceEventsReco"] = self.result_reinforce_events_real
		self.result_final["userLocations"] = self.userMainRegion
		self.result_statis_json = {
										"recoPerfectCnt" : self.statis_reco_perfect_cnt,
										"recoCantCnt" : self.statis_reco_cant_cnt,
										"recoNoLocaHasEventType" : self.statis_reco_no_loca_has_evnttype,
										"recoNoLovaNoEventType" : self.statis_reco_no_loca_no_evnttype ,
										"recoHasLocaNoEventType" : self.statis_reco_has_loca_no_evnttype,
										"reommendedCnt" :self.statis_recommended_cnt,
										"noRecommended_cnt":self.statis_no_recommended_cnt
										 
									}
		self.result_final["staticData"] = self.result_statis_json




	def __checkRecoStauts(self):
		reinforce = self.__reinforceFromExtracted()
		print("result=>"+ str(reinforce.event_reco_result))

		if reinforce.event_reco_result["code"] == 2 or reinforce.event_reco_result["code"] == 3 or reinforce.event_reco_result["code"] == 5  : 
		
			
			self.statis_no_recommended_cnt += 1

			self.result_reinforce_events_for_web.append(
											{
												"event_types":"비추천",
												"locations":"비추천"			
											}
										)			
		else:
			
			self.statis_recommended_cnt += 1  			
			self.result_reinforce_events_for_web.append(
											{
												"event_types" : self.__pretty_type(self.reinforce_json["event_types"]),
												"locations" : self.__pretty_locations(self.reinforce_json["locations"])														
											}
										)


		if reinforce.event_reco_result["code"] == 1:
			self.statis_reco_perfect_cnt += 1

		elif reinforce.event_reco_result["code"] == 2:	
			self.statis_reco_cant_cnt += 1

		elif reinforce.event_reco_result["code"] == 3:	
			self.statis_reco_no_loca_has_evnttype += 1

		elif reinforce.event_reco_result["code"] == 4:				
			self.statis_reco_no_loca_no_evnttype += 1

		elif reinforce.event_reco_result["code"] == 5:		
			self.statis_reco_has_loca_no_evnttype += 0

			
			
			
						


	def __reinforceFromExtracted(self):
		reinforce = Reinforce(self.extracted_json)
		
		#### TODO
		##!!!! user_event_hashkey를 가지고 mainRegion을 추출한다.
		### 실제 Extracted붙였을떄 확인해봐야한다!!!!
		##원래는 append에붙어있엇음...
		# self.user_event_hashkey = reinforce.event_reco_result["event_info_data"]["event_hashkey"]

		self.reinforce_json = reinforce.event_reco_result["event_info_data"]					
		self.result_reinforce_events_real.append(self.reinforce_json)
		return reinforce




			
			
	def __append_analaysis_events_for_web(self):
		self.result_analysis_events_for_web.append(
														{
															"event_types":self.__pretty_type(self.extracted_json["event_types"]),
															"locations":self.__pretty_locations(self.extracted_json["locations"]),
															"time_set":self.extracted_json["time_set"]	
														}
													)

	def __extractFromEvent(self):

		if self.event["location"] == None:
			self.event["location"] = ''
		

		print('extractor에게 넘겨주는 summary => ' + str(self.event["summary"]))
		print('extractor에게 넘겨주는 start_dt => ' + str(self.event["start_dt"]))
		print('extractor에게 넘겨주는 end_dt => ' + str(self.event["end_dt"]))
		print('extractor에게 넘겨주는 locataion => ' + str(self.event["location"]))

		#### TODO
		####False 일때 221 LINE을 확인해봐야한다!!!
		#실제 데이터 ..
		if self.switchExtractor == True:
			self.extracted_json = extract_info_from_event(self.event["event_hashkey"],self.event["summary"],self.event["start_dt"],self.event["end_dt"],self.event["location"])
		#목업 데이터 ..
		else:
			self.extracted_json = {
									    "event_hashkey":"ce5676473fc542e42dee19af6ed89617d73d4901f7a391bd30019a51",
									    "locations" :  [
									        {
									            "no" : 0,
									            "region" : "신사역"
									        }
									    ],
									    "time_set" : {
									      "extract_start": "18:00",
									      "extract_end": "19:00",
									      "event_start": "10:00",
									      "event_end": "11:00"
									    },
									    "event_types" : [
									        {
									            "id" : "CPI02"
									        }
									    ]
									}	

	def __appendEvent(self):
		self.user_event_hashkey = self.event["event_hashkey"]
		self.result_events.append(
						{
							"calendarName":self.calendar_name,
							"eventSummary":self.event["summary"],
							"eventStartDt":self.event["start_dt"],
							"eventEndDt":self.event["end_dt"],
							"eventLocation":self.event["location"],
						}
					)	


	def __getEventsList(self,calendar_hashkey):
		return utils.fetch_all_json(
			db_manager.query(
					"""
					SELECT * FROM EVENT 
					WHERE calendar_hashkey = %s 
					ORDER BY start_dt DESC
					""",							
					(calendar_hashkey,)
			)
		)		
	def __getCalendarList(self,account_hashkey):
		return utils.fetch_all_json(
			db_manager.query(
					"""
					SELECT * FROM CALENDAR
					WHERE account_hashkey = %s 
					
					""",							
					(account_hashkey,)
			)
		)		

	def __pretty_locations(self,extracted_locations):
		if extracted_locations == None or extracted_locations == 'Cannot':
			real_extracted_locations = extracted_locations				
		else :	
			real_extracted_locations = ''		
			for loca in extracted_locations:
				real_extracted_locations += loca["region"] + " "


		return real_extracted_locations

	def __pretty_type(self,extracted_event_types):
		if extracted_event_types == None :
			real_extracted_event_types = extracted_event_types	
		else:
			real_extracted_event_types = ''
			for e_type in extracted_event_types:						
				# print("test"+str(e_type)+" end")
				type_name = ''
				if str(e_type["id"]) == 'CPI01':
					type_name = '지인과의 약속'
				if str(e_type["id"]) == 'CPI02':
					type_name = '데이트'	
				if str(e_type["id"]) == 'CPI03':
					type_name = '기념일'		
				if str(e_type["id"]) == 'CPI04':
					type_name = '뒷풀이'			
				if str(e_type["id"]) == 'CPI05':
					type_name = '회의/스터디'										
				if str(e_type["id"]) == 'CPI06':
					type_name = '문화생활'		
				real_extracted_event_types += str(type_name) + " "	

		return real_extracted_event_types