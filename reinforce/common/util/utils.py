import hashlib
import time
import json
from time import gmtime, strftime
from datetime import datetime

def make_hashkey_nonetime(solt):
	soltt = str(solt+'secrettskkey')
	soltt = soltt.encode('utf-8')
	return hashlib.sha224(soltt).hexdigest()
def make_hashkey(solt):
	soltt = str(solt)+str(time.time()*1000)	
	soltt = soltt.encode('utf-8')
	return hashlib.sha224(soltt).hexdigest()
def fetch_all_json(result):
	lis = []

	for row in result.fetchall():
		i = 0
		dic = {}

		for data in row:
			if type(data) == datetime:
				dic[result.keys()[i]]= str(data)
			else:
				dic[result.keys()[i]]= data
			if i == len(row)-1:
				lis.append(dic)

			i=i+1
	return lis
