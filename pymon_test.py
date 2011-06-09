#encoding=UTF-8
import pymongo
import os

from pymongo import Connection

def read_file(log_file):
	"""read log file and format it to hash"""
	file = open(log_file,'r')
	result = []
	while 1:
		content = file.readline()
		if not content:
			break
		else:
			scon = content.split("\003")
			if len(scon) == 13:
				track = {'device_no' : scon[0], 'sim' : scon[1],'type' : scon[2],'gps_time' : scon[3],
						 'valid' : scon[4], 'long' : scon[5], 'lat' : scon[6], 'altitude' : scon[7],
						 'speed' : scon[8], 'course' : scon[9], 'km' : scon[10], 'para' : scon[11],
						 'rtime' : scon[12].strip()}
				result.append(track)
	file.close()
	return result

def list_file(path):
	"""docstring for list_file"""
	files = os.listdir(path)
	result = []
	for filename in files:
		if filename =='.DS_Store':
			files.remove(filename)
			continue
		filename = path+'/'+filename
		result.append(filename)
	return result

def conn_to_mongodb(coll_name):
	conn = Connection()
	db = conn.test
	coll = db[coll_name]
	return coll

def insert_into(data_set):
	""" save the data set into db """
	coll = conn_to_mongodb('track_log')
	coll.insert(data_set)

def get_coll_count():
	""""""
	coll = conn_to_mongodb('track_log')
	return coll.count()
	
def query_data(query_str):
	"""docstring for query_data"""
	coll = conn_to_mongodb('track_log')
	docs = coll.find(query_str)
	return docs

if __name__ == '__main__':
	# files =  list_file('/Users/fanwu/Desktop/trck')
	# for log_file in files:
	# 	data = read_file(log_file)
	# 	insert_into(data)
	# print("there is %d rows in table" % get_coll_count())
	docs = query_data({"device_no":"00318960390455"})
	for post in docs:
		print post["type"]
		