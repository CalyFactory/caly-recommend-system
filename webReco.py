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

	#account_hashkey와 extractor 옵션을 넣어준다.
	reco_maestro = recoMaestro.RecoMaestro(account_hashkey,False)
	
	return json.dumps(reco_maestro.result_final)
	





app.run(host='0.0.0.0', port = 9254, debug=True)
