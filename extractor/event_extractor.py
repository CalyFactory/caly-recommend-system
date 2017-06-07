import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import json
import string

from common import db_manager

import MeCab

def load_subway_dict():
	region_dict={}
	region_rows = db_manager.query('select station_name, old_address from SUBWAY_INFO')

	for row in region_rows:
		if type(row.old_address) is str:
			splited_address = row.old_address.split(' ')
			
			# 해당 키의 항목이 있으면, 해당 값에 append
			if splited_address[2] in region_dict:
				is_exist=False
				for item in region_dict[splited_address[2]]:
					if item == row.station_name+'역':
						is_exist=True
						break

				if is_exist is False:
					region_dict[splited_address[2]].append(row.station_name+'역')
			# 해당 키의 항목이 없으면, 새로운 리스트 형태로 추가
			else:
				region_dict[splited_address[2]]=[row.station_name+'역']
	extract_conf_dict={}
	with open('../key/extract_conf.json') as extract_conf_json:
		extract_conf_dict = json.load(extract_conf_json)


	for extra_region in extract_conf_dict["extra-region"].keys():
		region_dict[extra_region]=extract_conf_dict["extra-region"][extra_region]

	univ_dict={}
	univ_rows = db_manager.query('select univ_name, old_address from UNIV_INFO')

	for row in univ_rows:
		if type(row.old_address) is str:
			splited_address = row.old_address.split(' ')
		
			univ_dict[row.univ_name]=splited_address[2]

	return [region_dict, univ_dict]

def extract_info_from_event(event_hashkey,sentence,start_dt, end_dt, location):
	full_sentence=location+' '+sentence
	region_collect_dict, univ_collect_dict = load_subway_dict()
	
	location_count=0
	location_list=[]
	splited_start_dt=str(start_dt).split(' ')
	splited_end_dt=str(end_dt).split(' ')

	time_zone_dict={
		'event_start':'',
		'event_end':'',
		'event_start':splited_start_dt[1][:5],
		'event_end':splited_end_dt[1][:5]
	}
	purpose_count = {
		'CPI01':0,
		'CPI02':0,
		'CPI03':0,
		'CPI04':0,
		'CPI05':0,
		'CPI06':0
	}
	event_type_list=[]
	standard_time_scope={}
	extract_conf_dict={}
	with open('../key/extract_conf.json') as extract_conf_json:
		extract_conf_dict = json.load(extract_conf_json)
	standard_time_scope=extract_conf_dict["time-set"]
	
	cannot_recommend=False
	exist_time=False
	try:
	
		t = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ko-dic')
	
		t.parse(full_sentence)
		time = -1
		total_purpose_count=0
		m = t.parseToNode(full_sentence)
		while m:
			### Grep time-zone : ical / line_plus@naver.com
			if m.feature.find('SN') > -1 and m.surface.isdigit():
				time=m.surface
			elif m.feature.find('NNBC') > -1 and m.feature.find('시') > -1 and time is not -1:
				exist_time=True
				end_time = int(time)+1
				if int(time) < 10:
					time = '0'+str(time)
				if int(end_time) < 10:
					end_time = '0'+str(end_time)
				time_zone_dict['extract_start']=str(time)+':00'
				time_zone_dict['extract_end']=str(end_time)+':00'
			elif (m.surface.find('아침') > -1) or (m.surface.find('브런치') > -1) or (m.surface.find('점심') > -1) or (m.surface.find('저녁') > -1) or (m.surface.find('밤') > -1):
				time=standard_time_scope[m.surface]

			### Grep purpose
			elif m.feature.find('CPI') > -1:
				if total_purpose_count > 1:
					continue

				parts_of_feature = m.feature.split(',')
				for part in parts_of_feature:
					if part.find('CPI') > -1:
						if purpose_count[part] > 0:
							continue
						purpose_count[part]=purpose_count[part]+1
						event_type_list.append({"id":part})
						total_purpose_count=total_purpose_count+1
						#purposeResult=purposeResult+' '+print_purpose[part]

			### Grep location : google / calyfactorytester3@gmail.com
			elif (m.feature.find("대학교") > -1):
				if m.surface.find("대학교") > -1:
					#result=result+m.surface
					if m.surface in univ_collect_dict:
						# 첫번째 역으로 가정
						location_list.append({'no':location_count,'region':region_collect_dict[univ_collect_dict[m.surface]][0]})
						location_count = location_count + 1
					else:
						#print("Can't supported university.")
						cannot_recommend=True

						
				else:
					parts_of_feature = m.feature.split(',')
					#print(parts_of_feature)
					for part in parts_of_feature:
						if part.find('대학교') > 0:
							#result=result+part
							
							if part in univ_collect_dict:
								location_list.append({'no':location_count,'region':region_collect_dict[univ_collect_dict[part]][0]})
								location_count = location_count + 1
							else:
								#print("Can't supported university.")
								cannot_recommend=True
							continue	
			elif (m.feature.find("지하철") > -1) and (m.surface.find("역") < 0 or m.surface == '동역사'):
				parts_of_feature = m.feature.split(',')
				for part in parts_of_feature:
					if part.find('역') > -1:
						location_list.append({'no':location_count,'region':part})
						location_count = location_count + 1
						#result=result+part
						continue
			elif m.feature.find("지하철") > -1:
				location_list.append({'no':location_count,'region':m.surface})
				location_count = location_count + 1

			elif m.feature.find("동이름") > 0:
				#result=result+m.surface
				if m.surface in region_collect_dict:
					location_list.append({'no':location_count,'region':region_collect_dict[m.surface][0]})
					location_count = location_count + 1
				else:
					print("Can't supported sub-region.")
					cannot_recommend=True
			else:
				#print('else : '+m.surface+'/ '+m.feature)
				pass

			m = m.next

	except RuntimeError as e:
		print("RuntimeError:", e)


	if exist_time is False:
		time_zone_dict['extract_start']='None'
		time_zone_dict['extract_end']='None'
	if total_purpose_count is 0:
		event_type_list="None"

	if location_count is 0:
		location_list="None"
	if cannot_recommend is True:
		location_list="Cannot"

	return {
		'event_hashkey': event_hashkey,
		'locations': location_list,
		'time_set': time_zone_dict, 
		'event_types':event_type_list
	}


print(extract_info_from_event('hashkey1','test001','2017-07-04 12:00:00','2017-07-04 13:00:00',''))