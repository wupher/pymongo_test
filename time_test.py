#!/usr/env python
#--encoding: utf-8--
# I want to test if a datetime without tfz insert into mongodb will be auto transfer into UTC time correctlly
import pymongo
from datetime import datetime
from pymongo import Connection

conn = Connection()
db = conn.datetiem_test
coll = db['dt']

#empty data
coll.remove()

time = datetime.now()
print ("current insert time is: "+repr(time.hour)+":"+repr(time.minute))
data = {"memo":"python test data", "datetime":datetime.now()}
coll.insert(data)

data = coll.find_one()
print ("get time record is: " + repr(data["datetime"].hour) + ":"+repr( data["datetime"].minute))
