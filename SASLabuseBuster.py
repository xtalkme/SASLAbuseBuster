#!/usr/sbin/python

import re
import json
from pymongo import MongoClient


con = MongoClient("localhost", 27017)
db = con.postfix_database
sasl = db.sasl
posts = db.sasl


mylist = []

for line in open("smtplog"):
    if "sasl" in line:
        mylist.append(re.split('\s+', line))

lst = []

for item in mylist:
  d = {}
	d['Timestamp']=item[0] + " " + item[1] + " " + item[2]
	d['messageid']=item[5].strip(":")
	d['client']=re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", item[6]).group()
	d['method']=item[7].strip("sasl_method=").strip(",")
	d['username']=item[8].split("sasl_username=")[1]
	lst.append(d)



data = lst
def upload_mongo():
	posts = db.sasl
	for item in data:
		posts.insert(item, sort_keys=True, indent=4, separators=(',', ': '))
	return "JSON import succesfully posted to MongoDB"

upload_mongo()

