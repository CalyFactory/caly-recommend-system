import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import json
import string
from datetime import timedelta

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
	# 2017-07-04 12:00:00
	splited_start_dt=str(start_dt).split(" ")
	splited_end_dt=str(end_dt).split(" ")
	# 12:00:00
	time_set_dict={
		"event_start":"",
		"event_end":"",
		"event_start":splited_start_dt[1][:5],
		"event_end":splited_end_dt[1][:5]
	}
	# 12:00
	purpose_count = {
		"CPI01":0,
		"CPI02":0,
		"CPI03":0,
		"CPI04":0,
		"CPI05":0,
		"CPI06":0
	}
	event_type_list=[]
	standard_time_scope={}
	extract_conf_dict={}

	with open("../key/extract_conf.json") as extract_conf_json:
		extract_conf_dict = json.load(extract_conf_json)
	standard_time_scope=extract_conf_dict["time-set"]
	
	cannot_recommend=False
	exist_time=False
	try:
	
		t = MeCab.Tagger ("-d /usr/local/lib/mecab/dic/mecab-ko-dic")
	
		t.parse(full_sentence)
		time = -1
		number = -1
		total_purpose_count=0
		m = t.parseToNode(full_sentence)
		
		while m: 
			### Grep time-zone : ical / line_plus@naver.com
			if (m.surface.find("아침") > -1) or (m.surface.find("브런치") > -1) or (m.surface.find("점심") > -1) or (m.surface.find("저녁") > -1) or (m.surface.find("밤") > -1):
				time=standard_time_scope[m.surface]
			elif m.feature.find("SN") > -1 and m.surface.isdigit():
				number=m.surface
				# m.next 해서 그 다음 바로 시가 나오는지 체크?
				# 의존성 무시
			elif m.feature.find("NNBC") > -1 and m.feature.find("시") > -1 and number is not -1:
				exist_time=True 
				# 시를 한번 받고 나서 다음에 또 숫자와 시가 안나온 것을 체크하고 end time 가정해서 입력
				

				end_time = int(number)+1 # delta hour 등
				if int(time) < 10:
					time = "0"+str(time)
				if int(end_time) < 10: # 코드 반복
					end_time = "0"+str(end_time)
				# 뽑아내는 것은 format 기능으로, c언어 스트링 다루듯이 ( 예외처리 고려 X )
				time_set_dict["extract_start"]=str(time)+":00"
				time_set_dict["extract_end"]=str(end_time)+":00"
			

			### Grep purpose
			elif m.feature.find("CPI") > -1:
				cpi = m.feature.split(",")[3]
				if cpi.find("CPI") > -1:
					if purpose_count[cpi] == 0:
						event_type_list.append({"id":cpi})
					purpose_count[cpi]=purpose_count[cpi]+1
						
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
		# raise exception
		# https://github.com/CalyFactory/caly/blob/develop/caldavclient/util.py
		# Except 발생 시, 죽어야되는건지, 값을 보정해줘야되는건지, 예외적인 상황을 반환해야되는건지, 다른 값으로 대체해야되는건지


	# Docs 참고
	if exist_time == False:
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

#print(extract_info_from_event("-","신촌 데이트","2017-07-04 12:00:00","2017-07-04 13:00:00",""))