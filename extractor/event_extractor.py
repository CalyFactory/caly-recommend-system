import os
root_path = os.path.dirname(os.path.dirname(__file__))

import json
import string
from datetime import datetime, date, time, timedelta
import pprint

EXTRACTOR_CONF_JS = "../key/extract_conf.json"
os.environ["CALY_DB_CONF"] = "../key/conf.json"
from common import db_manager

import MeCab


def load_subway_dict():
	region_dict={}
	region_rows = db_manager.query("select station_name, old_address from SUBWAY_INFO")

	for row in region_rows:
		if type(row.old_address) is str:
			splited_address = row.old_address.split(" ")
			
			# 해당 키의 항목이 있으면, 해당 값에 append
			if splited_address[2] in region_dict:
				is_exist=False
				for item in region_dict[splited_address[2]]:
					if item == row.station_name+"역":
						is_exist=True
						break

				if is_exist is False:
					region_dict[splited_address[2]].append(row.station_name+"역")
			# 해당 키의 항목이 없으면, 새로운 리스트 형태로 추가
			else:
				region_dict[splited_address[2]]=[row.station_name+"역"]
	extract_conf_dict={}
	with open(EXTRACTOR_CONF_JS) as extract_conf_json:
		extract_conf_dict = json.load(extract_conf_json)


	for extra_region in extract_conf_dict["extra-region"].keys():
		region_dict[extra_region]=extract_conf_dict["extra-region"][extra_region]

	univ_dict={}
	univ_rows = db_manager.query("select univ_name, old_address from UNIV_INFO")

	for row in univ_rows:
		if type(row.old_address) is str:
			splited_address = row.old_address.split(" ")
		
			univ_dict[row.univ_name]=splited_address[2]

	return [region_dict, univ_dict]

def extract_info_from_event(event_hashkey,summary,start_dt, end_dt, location):
	full_sentence=location+" "+summary
	region_collect_dict, univ_collect_dict = load_subway_dict()
	# pp = pprint.PrettyPrinter(indent=4)
	# pp.pprint(region_collect_dict)
	location_list=[]
	
	py_start_dt = datetime.strptime(start_dt, "%Y-%m-%d %H:%M:%S")
	py_end_dt = datetime.strptime(end_dt, "%Y-%m-%d %H:%M:%S")
	py_dt = None

	time_set_dict={
		"event_start":"",
		"event_end":"",
		"event_start":py_start_dt.strftime("%H:%M"),
		"event_end":py_end_dt.strftime("%H:%M")
	}
	korean_time_dict={
		"한":1,
		"두":2,
		"세":3,
		"네":4,
		"다섯":5,
		"여섯":6,
		"일곱":7,
		"여덟":8,
		"아홉":9,
		"열":10
	}
	event_type_count = {
		"CPI01":0,
		"CPI02":0,
		"CPI03":0,
		"CPI04":0,
		"CPI05":0,
		"CPI06":0
	}
	event_type_list=[]

	expect_dt=None
	expect_time_scope={}
	time_list=[]

	extract_conf_dict={}
	with open(EXTRACTOR_CONF_JS) as extract_conf_json:
		extract_conf_dict = json.load(extract_conf_json)
	expect_time_scope=extract_conf_dict["time-set"]
	represent_dict = extract_conf_dict["represent-region"]

	cannot_recommend=False

	try:
		t = MeCab.Tagger ("-d /usr/local/lib/mecab/dic/mecab-ko-dic")
	
		t.parse(full_sentence)
		number = None
		ten_number = 0 # 한/두/세 시

		m = t.parseToNode(full_sentence)
		
		while m: 
			""" 
			print()
			print(full_sentence)
			print(m.surface + ' / '+m.feature)
			print()"""
			### Grep time
			if m.surface.find("아침") > -1 or m.surface.find("브런치") > -1 or m.surface.find("점심") > -1 or m.surface.find("저녁") > -1 or m.surface.find("밤") > -1:
				expect_dt=datetime.strptime(expect_time_scope[m.surface], "%H:%M")

				# Additional event type
				if event_type_count["CPI01"] == 0:
					event_type_list.append({"id":"CPI01"})
				event_type_count["CPI01"]=event_type_count["CPI01"]+1
			elif m.feature.find("SN") > -1 and m.surface.isdigit():
				number = m.surface
			elif m.feature.find("NR,*,T,열") > -1:
				ten_number=10
				number=ten_number
			elif m.feature.find("MM,~가산명사") > -1 or m.feature.find("NR") > -1:
				single_number = 0
				if m.surface in korean_time_dict:
					single_number=korean_time_dict[m.surface]
					number = ten_number + single_number
			elif m.feature.find("NNBC") > -1 and m.feature.find("시") > -1 and number != None:
				if int(number) < 6:
					number = int(number) + 12
				elif len(time_list) == 1:
					prev_dt = datetime.strptime(time_list[0], "%H:%M")
					if int(prev_dt.strftime("%H")) > 12 and int(number) < 12:
						number = int(number) + 12

				str_number = str(number)
				py_dt=datetime.strptime(str_number, "%H")
				time_list.append( py_dt.strftime("%H:%M"))
				number = None
			elif m.feature.find("NNBC") > -1 and m.feature.find("분") > -1 and number != None and py_dt != None:
				time_list[ len(time_list)-1 ] = datetime.strptime(py_dt.strftime("%H")+":"+number, "%H:%M").strftime("%H:%M")
				number = None
				py_dt=None
			elif m.surface.find("반") > -1 and py_dt != None:
				time_list[ len(time_list)-1 ] = datetime.strptime(py_dt.strftime("%H")+":30", "%H:%M").strftime("%H:%M")
				py_dt=None

			### Grep event type
			elif m.surface.find("CGV") > -1:
				if event_type_count["CPI06"] == 0:
					event_type_list.append({"id":"CPI06"})
				event_type_count["CPI06"]=event_type_count["CPI06"]+1
			
			elif m.feature.find("CPI") > -1:
				cpi = m.feature.split(",")[3]
				if cpi.find("CPI") > -1:
					if event_type_count[cpi] == 0:
						event_type_list.append({"id":cpi})
					event_type_count[cpi]=event_type_count[cpi]+1
						
			### Grep location : google / calyfactorytester3@gmail.com
			elif m.feature.find("대표지이름") > -1 and len(location_list) < 1:

				if m.surface in represent_dict:
					location_list.append({"no":len(location_list),"region":represent_dict[m.surface]})
				else:
					cannot_recommend=True
					location_list.append({"no":len(location_list),"region":m.surface})

			elif m.feature.find("대학교") > -1 and len(location_list) < 1:
				if m.surface.find("대학교") > -1:
					# only supported university
					if m.surface in univ_collect_dict:
						# 첫번째 역으로 가정
						location_list.append({"no":len(location_list),"region":region_collect_dict[univ_collect_dict[m.surface]][0]})
					else:
						cannot_recommend=True
						location_list.append({"no":len(location_list),"region":m.surface})

				else:
					univ = m.feature.split(",")[7]
					if (univ.find("대학교") > 0) and (univ in univ_collect_dict):
						location_list.append({"no":len(location_list),"region":region_collect_dict[univ_collect_dict[univ]][0]})
					else:
						cannot_recommend=True
						location_list.append({"no":len(location_list),"region":m.surface})
	
			elif m.feature.find("지하철") > -1 and m.surface.find("역") == -1 and len(location_list) < 1:
				subway = m.feature.split(",")[7]
				if subway.find("역") > -1:
					location_list.append({"no":len(location_list),"region":subway})

			elif m.feature.find("지하철") > -1 and len(location_list) < 1:
				location_list.append({"no":len(location_list),"region":m.surface})

			elif m.feature.find("동이름") > 0 and len(location_list) < 1:	
				# only supported sub-region
				if m.surface in region_collect_dict:
					location_list.append({"no":len(location_list),"region":region_collect_dict[m.surface][0]})
				else:
					cannot_recommend=True
					location_list.append({"no":len(location_list),"region":m.surface})

			m = m.next

	except RuntimeError as e:
		print("RuntimeError:", e)
		raise Exception('Event parsing error '+ str(e))
		# https://github.com/CalyFactory/caly/blob/develop/caldavclient/util.py
	if expect_dt != None:
		time_set_dict["extract_start"]=expect_dt.strftime("%H:%M")
		expect_date = str(expect_dt.strftime("%H:%M"))
		expect_end_dt = datetime.strptime(expect_date,"%H:%M") + timedelta(hours=1)
		time_set_dict["extract_end"]=expect_end_dt.strftime("%H:%M")
	if len(time_list) == 2:
		time_set_dict["extract_start"]=time_list[0]
		time_set_dict["extract_end"]=time_list[1]
	elif len(time_list) == 1:
		time_set_dict["extract_start"]=time_list[0]
		origin_date = str(time_list[0])
		extract_end_dt = datetime.strptime(origin_date,"%H:%M") + timedelta(hours=1)
		time_set_dict["extract_end"]=extract_end_dt.strftime("%H:%M")
	elif len(time_list) == 0 and expect_dt == None:
		time_set_dict["extract_start"]=None
		time_set_dict["extract_end"]=None

	if len(event_type_list) < 1:
		event_type_list=None
	if len(location_list) == 0:
		location_list=None
	

	
	return {
		"event_hashkey": event_hashkey,
		"cannot_reco": cannot_recommend,
		"locations": location_list,
		"time_set": time_set_dict, 
		"event_types":event_type_list
	}

#print(extract_info_from_event("-","한시 반 영어회화","2017-07-04 12:00:00","2017-07-04 13:00:00","합정"))