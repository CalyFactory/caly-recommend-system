import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import json
import string
from datetime import datetime, date, time

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
	with open("../key/extract_conf.json") as extract_conf_json:
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

	event_type_count = {
		"CPI01":0,
		"CPI02":0,
		"CPI03":0,
		"CPI04":0,
		"CPI05":0,
		"CPI06":0
	}
	event_type_list=[]

	standard_time_scope={}
	time_list=[]

	extract_conf_dict={}
	with open("../key/extract_conf.json") as extract_conf_json:
		extract_conf_dict = json.load(extract_conf_json)
	standard_time_scope=extract_conf_dict["time-set"]
	
	cannot_recommend=False

	try:
	
		t = MeCab.Tagger ("-d /usr/local/lib/mecab/dic/mecab-ko-dic")
	
		t.parse(full_sentence)
		time = -1
		number = None
		m = t.parseToNode(full_sentence)
		
		while m: 
			#print(m.surface + ' - '+m.feature)

			"""
			### Grep time-zone : ical / line_plus@naver.com
			if (m.surface.find("아침") > -1) or (m.surface.find("브런치") > -1) or (m.surface.find("점심") > -1) or (m.surface.find("저녁") > -1) or (m.surface.find("밤") > -1):
				number=standard_time_scope[m.surface]
			elif m.feature.find("SN") > -1 and m.surface.isdigit():
				number=m.surface
			elif m.feature.find("NNBC") > -1 and m.feature.find("시") > -1 and number is not -1:
				exist_time=True 
				# 시를 한번 받고 나서 다음에 또 숫자와 시가 안나온 것을 체크하고 end time 가정해서 입력
				
				end_time = int(number)+1 # delta hour 등
				if int(number) < 10:
					number = "0"+str(number)
				if int(end_time) < 10: # 코드 반복
					end_time = "0"+str(end_time)
				
				time_set_dict["extract_start"]=str(number)+":00"
				time_set_dict["extract_end"]=str(end_time)+":00"
			"""
			# datetime.strptime(end_dt, "%Y-%m-%d %H:%M:%S")
			# py_end_dt.strftime("%H:%M")
			if (m.surface.find("아침") > -1) or (m.surface.find("브런치") > -1) or (m.surface.find("점심") > -1) or (m.surface.find("저녁") > -1) or (m.surface.find("밤") > -1):
				py_dt=datetime.strptime(standard_time_scope[m.surface], "%H:%M")
			elif m.feature.find("SN") > -1 and m.surface.isdigit():
				number = m.surface
			elif m.feature.find("NNBC") > -1 and m.feature.find("시") > -1 and number != None:
				py_dt=datetime.strptime(number, "%H")

				time_list.append( py_dt.strftime("%H:%M"))
				number = None
			elif m.feature.find("NNBC") > -1 and m.feature.find("분") > -1 and number != None and py_dt != None:
				#py_dt=datetime.strptime(number, "%M") without keeping value
				time_list[ len(time_list) ] = datetime.strptime(py_dt.strftime("%H")+":"+number, "%H:%M") 
				number = None
				py_dt=None

			### Grep purpose
			if m.feature.find("CPI") > -1:
				cpi = m.feature.split(",")[3]
				if cpi.find("CPI") > -1:
					if event_type_count[cpi] == 0:
						event_type_list.append({"id":cpi})
					event_type_count[cpi]=event_type_count[cpi]+1
						
			### Grep location : google / calyfactorytester3@gmail.com
			elif (m.feature.find("대학교") > -1) and len(location_list) < 1:
				if m.surface.find("대학교") > -1:
					# only supported university
					if m.surface in univ_collect_dict:
						# 첫번째 역으로 가정
						location_list.append({"no":len(location_list),"region":region_collect_dict[univ_collect_dict[m.surface]][0]})

				else:
					univ = m.feature.split(",")[3]
					if (univ.find("대학교") > 0) and (part in univ_collect_dict):
						location_list.append({"no":len(location_list),"region":region_collect_dict[univ_collect_dict[univ]][0]})
	
			elif (m.feature.find("지하철") > -1) and (m.surface.find("역") == -1) and (len(location_list) < 1):
				subway = m.feature.split(",")[7]
				if subway.find("역") > -1:
					location_list.append({"no":len(location_list),"region":subway})

			elif (m.feature.find("지하철") > -1) and (len(location_list) < 1):
				location_list.append({"no":len(location_list),"region":m.surface})

			elif (m.feature.find("동이름") > 0) and ( len(location_list) < 1 ):	
				# only supported sub-region
				if m.surface in region_collect_dict:
					location_list.append({"no":len(location_list),"region":region_collect_dict[m.surface][0]})



			m = m.next

	except RuntimeError as e:
		print("RuntimeError:", e)
		raise Exception('Event parsing error '+ str(e))
		# https://github.com/CalyFactory/caly/blob/develop/caldavclient/util.py

	# Docs 참고
	# if time_list.length == 1 set end_time
	if len(time_list) == 2:
		time_set_dict["extract_start"]=time_list[0]
		time_set_dict["extract_end"]=time_list[1]
	elif len(time_list) == 1:
		time_set_dict["extract_start"]=time_list[0]
		print('datetime.strptime(time_list[0], "%H:%M")+datetime.timedelta(days=1)')
		#print(datetime.strptime(time_list[0], "%H:%M")+datetime.timedelta(hour=1))
		print()
		#time_set_dict["extract_end"]=(datetime.strptime(time_list[0], "%H:%M")+datetime.timedelta(days=1)).strftime("%H:%M")
	else:
		time_set_dict["extract_start"]=None
		time_set_dict["extract_end"]=None
	if len(event_type_list) < 1:
		event_type_list=None
	if len(location_list) == 0:
		location_list=None
	
	
	return {
		"event_hashkey": event_hashkey,
		"locations": location_list,
		"time_set": time_set_dict, 
		"event_types":event_type_list
	}

#print(extract_info_from_event("-","강남 7시 소리랑 데이트","2017-07-04 12:00:00","2017-07-04 13:00:00",""))