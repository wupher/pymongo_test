#!/usr/bin/env python
# encoding: utf-8
"""
pymongo_test.py

Created by Fan Wu on 2011-06-17.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import pymongo
import re
from datetime import datetime
from pymongo import Connection

class MongoTrack(object):
	"""docstring for MongoTrack"""
	def __init__(self, db_host, db_port, database_name, collection_name, log_dir):
		super(MongoTrack, self).__init__()
		self.conn = self.connect_mongodb(db_host, db_port, database_name, collection_name)
		self.log_files = self.list_dir(log_dir)
	
	@staticmethod
	def read_file(log_file):
		"""read the log file content"""
		file = open(log_file, 'r')
		result = []
		while 1:
			content = file.readline()
			if not content:
				break
			else:
				data = content.split("\003")
				if len(data) == 13:
					track = {
							 'device_no' : long(data[0][3:]), 'sim' : data[1], 'type':int(data[2]), 'gps_time' : MongoTrack.time_trans(data[3]),
							 'valid' : data[4], 'loc':{'long' : float(data[5]), 'lat' : float(data[6]) }, 'altitude' : float(data[7]),
							 'speed' : float(data[8]), 'course' : float(data[9]), 'km' : float(data[10]), 'para' : float(data[11]),
							 'rtime' : MongoTrack.time_trans(data[12].strip())
							}
					result.append(track)
		file.close()
		return result
	
	@staticmethod
	def time_trans(datetime_str):
		"""transfer date string into datetime format"""
		if re.compile("(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)").match(datetime_str):
			return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
		
	
	@staticmethod
	def list_dir(log_dir):
		"""docstring for list_dir"""
		files = os.listdir(log_dir)
		result = []
		for filename in files:
			if filename == ".DS_Store":
				continue
			else:
				result.append(log_dir+'/'+filename)
		return result
	
	@staticmethod
	def connect_mongodb(host, port, database, collection):
		"""connect to mongodb"""
		return Connection(host, port)[database][collection]
	
	def count(self):
		"""docstring for count"""
		return self.count()
		
	def import_data(self):
		"""import all the track log data into the database"""
		if not self.log_files or len(self.log_files) ==0:
			print "There is no log files need to import into database"
		else:
			for log_file in self.log_files:
				data = self.read_file(log_file)
				self.conn.insert(data)
		
		
	def query(self,dict):
		"""docstring for query"""
		return self.conn.find(dict)
		
		
def main():
	mongo = MongoTrack('localhost',27017, 'time_test','python','/Users/fanwu/workspace/data/timetest')
	mongo.import_data()


if __name__ == '__main__':
	main()

