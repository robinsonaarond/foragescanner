#! /usr/bin/env python

# Hold getClass, which polls the database, then parses the description and supplies
# a classification based on that description.  For unsure guess, will place ? in
# front of the given class.

import sqlite3 as lite
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

myDB = "/Users/aaronr/Documents/fs_raspberrypi_contents/root/home/fs/Documents/fs.db"

def getClass(test):
	try:
		con = None
		con = lite.connect(myDB)
		cur = con.cursor()
	### First get list of classifications
		sqlquery = "select class from classifications"
		try:
			cur.execute(sqlquery)
			classes = cur.fetchall()
		except Exception, e:
			print e
			classes = ""
			pass
	### Get list of DB descriptions that don't have classifications
		#sqlquery = "select description from food where classification is null"
		sqlquery = "select description from food"
		try:
			cur.execute(sqlquery)
			descriptions = cur.fetchall()
		except Exception, e:
			print e
			descriptions = ""
			pass
	except Exception, e:
		print e
		pass
	### Guess classifications and add into database
	#		- Classes should be case/syntax insensitive (e.g., "Black Beans" = "black beans" = "black_beans")
	#for desc in descriptions:
		#print fuzz.partial_ratio(classes[0], desc), classes[0], desc
	desc_list = [x[0] for x in descriptions]
	class_list = [x[0] for x in classes]
	for myclass in class_list:
		cls = myclass.upper()
		print cls, process.extract(cls, desc_list, limit=1)	
	return 0

