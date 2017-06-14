# #-*- coding: utf-8 -*-


import os
import sys
root_path = os.path.dirname(os.path.dirname(__file__));


from pymongo import MongoClient

import json 
import sys

if 'test' not in sys.argv:

    with open(os.environ["CALY_DB_CONF"]) as conf_json:
        conf = json.load(conf_json)
    client = MongoClient('mongodb://'+conf["mongo"]["user"]+':' + conf["mysql"]["password"] + '@127.0.0.1')
    base_db = client.calydb
# >>>>>>> c86396f9855b30252acaf3b787507e8b4cb7e5fe

    #fcm log
    fcm = base_db.fcm
    #event관련 log
    event_log = base_db.event_log

    reco_log = base_db.reco_log


    account_list_log = base_db.account_list_log

    screen_log = base_db.screen_log
