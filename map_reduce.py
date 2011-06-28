#!/usr/bin/env python
# encoding: utf-8
"""
map_reduce.py

Created by Fan Wu on 2011-06-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
from pymongo import Connection
from bson.code import Code

def map_reduce():
	conn = Connection('localhost')['int_test']['track_log']
	
	"""docstring for map_reduce"""
	map = Code("function (){"
				"emit(this.device_no, 1);"
	"}")
	
	reduce = Code("function (key, values) {"
		"var x = 0;"
		"values.forEach( function(v) {x += v});"
		"return x;"
	"}")
	
	result = conn.map_reduce(map, reduce, "map_results")
	for doc in result.find():
		print doc
	
	

def main():
	map_reduce()


if __name__ == '__main__':
	main()

