#!/usr/bin/env python
# encoding: utf-8
"""
web.py

Created by Fan Wu on 2011-06-07.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
from flask import Flask, request
from flask import render_template
from pymongo import Connection

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def index():
	"""docstring for index"""
	return render_template("index.html")
	
	
@app.route('/query', methods=['GET','POST'])
def query():
	"""docstring for query"""
	if request.method == 'POST':
		name = request.form['name']
		value = request.form['value']
		docs = query_data({name:value})
		return render_template("result.html", docs=docs)
	return "ERROR"
	
def query_data(query_str):
	"""docstring for query_data"""
	coll = conn_to_mongodb('track_log')
	docs = coll.find(query_str)
	return docs	

def conn_to_mongodb(coll_name):
	conn = Connection()
	db = conn.test
	coll = db[coll_name]
	return coll
		
def main():	
	app.run(debug=True)


if __name__ == '__main__':
	main()

