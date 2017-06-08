import pprint
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

import recoMaestro

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
				ORDER BY user_id							
				""",							
		)
	)

	for row in rows:

				

		cal = utils.fetch_all_json(
			db_manager.query(
					"""
					SELECT * FROM CALENDAR AS c, EVENT AS e
					WHERE account_hashkey = %s
					AND c.calendar_hashkey = e.calendar_hashkey
					""",
					(row["account_hashkey"],)							
			)
		)
		if len(cal) != 0:

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
	# user_event_hashkey = ''
	reco_maestro = recoMaestro.RecoMaestro()
	calendars = reco_maestro.getCalendarList(account_hashkey)	
	pprint.pprint(calendars)

	for calendar in calendars:
		reco_maestro.calendar_hashkey = calendar["calendar_hashkey"]
		reco_maestro.calendar_name = calendar["calendar_name"]
		
		events = reco_maestro.getEventsList(reco_maestro.calendar_hashkey)
		
		#1. 캘린더당 몇개의 이벤트가 있는가.
		#2. 이벤트중  oo/xo/ox/xx인 경우는 몇가지인가.
		#3. 
		#캘린더의 이름입니다.
		calendar_name =  reco_maestro.calendar_name
		#이벤트의 카운트입니다. 
		eventsCnt = len(events)		

		for event in events:
			if 'summary' in event:
				print("events ==> "+str(event))
				reco_maestro.event = event
				reco_maestro.appendEvent()				

				reco_maestro.extractFromEvent()

				print("extcted_json => "+ str(reco_maestro.extracted_json))

				reco_maestro.append_analaysis_events_for_web()

				reco_maestro.checkRecoStauts()

	reco_maestro.getUserMainRegion()
	reco_maestro.makeFinalReuslt()

	print("staticsJson ->"+str(reco_maestro.result_statis_json))
	
	return json.dumps(reco_maestro.result_final)
	





app.run(host='0.0.0.0', port = 9254, debug=True)
