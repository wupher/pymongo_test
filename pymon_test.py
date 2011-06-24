#!/usr/bin/python
import pymongo
import os
import re
from pymongo import Connection
from datetime import datetime

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
				track = {
						 'device_no' : int(scon[0])[3:], 'sim' : scon[1], 'type':int(scon[2]), 'gps_time' : time_trans(scon[3]),
						 'valid' : scon[4], 'loc':{'long' : float(scon[5]), 'lat' : float(scon[6]) }, 'altitude' : float(scon[7]),
						 'speed' : float(scon[8]), 'course' : float(scon[9]), 'km' : float(scon[10]), 'para' : scon[11],
						 'rtime' : time_trans(scon[12].strip())
						}
				result.append(track)
	file.close()
	return result
	
def time_trans(time_str):
	"""trans the datetime string to datetime obj"""
	p = re.compile("(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)")
	if p.match(time_str):
		return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

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

def conn_to_mongodb(database, collection):
	conn = Connection()
	db = conn[database]
	coll = db[collection]
	return coll

def insert_into(database, collection, data_set):
	""" save the data set into db """
	coll = conn_to_mongodb(database, collection)
	coll.insert(data_set)

def get_coll_count():
	""""""
	coll = conn_to_mongodb('time_test','python')
	return coll.count()
	
def query_data(query_str):
	"""docstring for query_data"""
	coll = conn_to_mongodb('track_log')
	docs = coll.find(query_str)
	return docs

if __name__ == '__main__':
	print("Before Insert, there are %d rows in table" % get_coll_count())
	# files =  list_file('/Users/fanwu/workspace/data/timetest')
	# for log_file in files:
	data = read_file('/Users/fanwu/workspace/data/timetest/Trck003_20110429091832.log')

	insert_into("time_test","python",data)
	print("Finally, there is %d rows in table" % get_coll_count())
