
import flask 
from flask import redirect
from flask import render_template
from flask import request
from flask import make_response
from flask import session
from flask import send_from_directory
from common import db_manager
from common.util import utils
from extractor.event_extractor import extract_info_from_event
from reinforce.reinforce import Reinforce
from reco.reco import Reco
from flask_cors import CORS

import json
app = flask.Flask(__name__, static_url_path='')
CORS(app)

@app.route("/", methods = ["GET"])
def index(): 

	users = []
	rows = utils.fetch_all_json(
		db_manager.query(
				"""
				SELECT * FROM USERACCOUNT 
				WHERE user_id != 'None'				
				""",							
		)
	)	
	for row in rows:
		users.append(
						{
							"email":row["user_id"],
							"loginPlatform":row["login_platform"],
							"accountHashkey":row["account_hashkey"]
						}
					)
	print(users)


	return render_template('index.html',
							users = users)

def prettyLocations(extracted_locations):
	if extracted_locations == 'None' or extracted_locations == 'Cannot':
		real_extracted_locations = extracted_locations				
	else :	
		real_extracted_locations = ''		
		for loca in extracted_locations:
			real_extracted_locations += loca["region"] + " "


	return real_extracted_locations

def prettyType(extracted_event_types):
	if extracted_event_types == 'None' :
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

@app.route("/eventsDetail", methods = ["GET"])
def eventsDetail(): 
	reinforceEventsReco = request.args['eventDetail']
	print(reinforceEventsReco)
	reco_module = Reco(json.loads(reinforceEventsReco))

	return json.dumps(reco_module.get_reco_list(),ensure_ascii=False)

@app.route("/events", methods = ["GET"])
def events(): 
	account_hashkey = request.args['accountHashkey']
	result_events = []
	result_analysis_events = []
	result_sum = {}
	result_reinforce_events = []
	result_reinforce_events_real = []

	calendars = utils.fetch_all_json(
		db_manager.query(
				"""
				SELECT * FROM CALENDAR
				WHERE account_hashkey = %s 
				
				""",							
				(account_hashkey,)
		)
	)

	for calendar in calendars:
		calendar_hashkey = calendar["calendar_hashkey"]
		calendar_name = calendar["calendar_name"]
		events = utils.fetch_all_json(
			db_manager.query(
					"""
					SELECT * FROM EVENT 
					WHERE calendar_hashkey = %s
					""",							
					(calendar_hashkey,)
			)
		)
		
		for event in events:
			if 'summary' in event:
				# print("events ==>> "+str(event))
				event_summary = event["summary"]
				event_start_dt = event["start_dt"]
				event_end_dt = event["end_dt"]
				event_location = event["location"]
				event_hashkey = event["event_hashkey"]

				result_events.append(
								{
									"calendarName":calendar_name,
									"eventSummary":event_summary,
									"eventStartDt":event_start_dt,
									"eventEndDt":event_end_dt,
									"eventLocation":event_location,
								}
							)
				if event_location == None:
					event_location = ''
				# print(event_summary)
				# print(event_start_dt)
				# print(event_end_dt)
				# print(event_location)
				try:
					extracted_json = extract_info_from_event(event_hashkey,event_summary,event_start_dt,event_end_dt,event_location)
				except Exception as e:
					print('error!!>>'+str(e))

				# print('extraced_json =>'+str(extracted_json))

				extracted_locations = extracted_json["locations"]
				extracted_event_types = extracted_json["event_types"]
				extracted_time_set = extracted_json["time_set"]

				
				real_extracted_locations = prettyLocations(extracted_locations)					


				real_extracted_event_types = prettyType(extracted_event_types)

				result_analysis_events.append(
												{
													"event_types":real_extracted_event_types,
													"locations":real_extracted_locations,
													"time_set":extracted_time_set
												}
											)
				reinforce = Reinforce(extracted_json)
				# print("recoResult = > "+ str(reinforce.event_reco_result))
				reinforce_json = reinforce.event_reco_result["event_info_data"]					
				result_reinforce_events_real.append(reinforce_json)

				if reinforce.event_reco_result["code"] != 2 :

					reinforce_locations = reinforce_json["locations"]
					reinforce_event_types = reinforce_json["event_types"]

					real_reinforce_locations = prettyLocations(reinforce_locations)					
					real_reinforce_event_types = prettyType(reinforce_event_types)	
					# print(real_reinforce_locations)
					# print(real_reinforce_event_types)
					result_reinforce_events.append(
													{
														"event_types":real_reinforce_event_types,
														"locations":real_reinforce_locations													
													}
												)

				else:
					result_reinforce_events.append(
													{
														"event_types":"-",
														"locations":"-"			
													}
												)	

	result_sum["originEvents"] = result_events
	result_sum["analysisEvents"] = result_analysis_events
	result_sum["reinforceEvents"] = result_reinforce_events
	result_sum["reinforceEventsReco"] = result_reinforce_events_real



	return json.dumps(result_sum)





app.run(host='0.0.0.0', port = 9254, debug=True)
