#!/usr/bin/env python
# encoding: utf-8
"""
date_dump.py

Created by 范武 on 2011-07-25.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import random
import time
from pymongo import Connection
from datetime import datetime

def generate_track():
	"""generate track data by calc"""
	phone = 18905900000 + random.randint(0,20000)
	loc = {'lat' : 24 + random.random(), 'long' :  118 + random.random()}
	return {'device_no' : phone, 'loc' : loc, 'GPS_time' : datetime.now(), 'valid' : 'A', 'altitude' : 38, 
	'speed' : random.randint(0, 150), 'navigation_course' : 0, 'KM' : random.randint(0, 10000), 'parameter' : 1031,
	'recv_time' : datetime.now(), 'type' : 2}
	
def update_track(collection):
	"""update track with phone number"""
	for i in  range(6666) :
		track = generate_track()
		# track["_id"] = track["device_no"] 
		#貌似python drvier不允许我指定_id，否则就会无法插入
		collection.update({"device_no" : track["device_no"]}, {"$set" : track}, upsert=True)

	

def main():
	coll = Connection().test.data
	while True:
		stamp = datetime.now()
		update_track(coll)
		used_time = (datetime.now() - stamp).total_seconds()
		gap = 60 - used_time
		if gap > 0:
			print("in time: %f, used time: %f" % (gap, used_time))
		else:
			print("out of time: %f, used time: %f" % (gap, used_time))
	

if __name__ == '__main__':
	main()

