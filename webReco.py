
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

import webMaestro

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
	# print(users)


	return render_template('index.html',
							users = users)



@app.route("/eventsDetail", methods = ["GET"])
def eventsDetail(): 
	reinforceEventsReco = request.args['eventDetail']
	print(reinforceEventsReco)
	reco_module = Reco(json.loads(reinforceEventsReco))

	return json.dumps(reco_module.get_reco_list(),ensure_ascii=False)

@app.route("/events", methods = ["GET"])
def events(): 

	account_hashkey = request.args['accountHashkey']

	# #실제 유저 이벤트
	# result_events = []
	# #[웹뷰용]형태소분석 된 이후 분석된 이벤트 정보를 웹뷰에 보여주기위한 데이터
	# result_analysis_events_for_web = []
	# #최종 웹에 보여줄 데이터
	# result_final= {}
	# #[웹뷰용]보강된 데이터 넘겨줄 배열
	# result_reinforce_events_for_web = []
	# #실제 넘길데이터
	# result_reinforce_events_real = []

	# calendars = utils.fetch_all_json(
	# 	db_manager.query(
	# 			"""
	# 			SELECT * FROM CALENDAR
	# 			WHERE account_hashkey = %s 
				
	# 			""",							
	# 			(account_hashkey,)
	# 	)
	# )
	
	# user_event_hashkey = ''
	web_maestro = webMaestro.WebMaestro()
	calendars = web_maestro.getCalendarList(account_hashkey)	

	for calendar in calendars:
		web_maestro.calendar_hashkey = calendar["calendar_hashkey"]
		web_maestro.calendar_name = calendar["calendar_name"]
		
		events = web_maestro.getEventsList(web_maestro.calendar_hashkey)
		# print("events ==> "+str(events))
		for event in events:
			if 'summary' in event:
				print("events ==> "+str(event))

				web_maestro.event = event
				web_maestro.appendEvent()				

				web_maestro.extractFromEvent()

				print("extcted_json => "+ str(web_maestro.extracted_json))

				web_maestro.append_analaysis_events_for_web()

				web_maestro.checkRecoStauts()

	web_maestro.getUserMainRegion()
	web_maestro.makeFinalReuslt()
	# print("final web Return result"+str(web_maestro.result_final))
	return json.dumps(web_maestro.result_final)
	# return 'hi'





app.run(host='0.0.0.0', port = 9254, debug=True)
