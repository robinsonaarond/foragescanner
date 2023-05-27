#! /usr/bin/env python

# Hold getClass, which polls the database, then parses the description and supplies
# a classification based on that description.  For unsure guess, will place ? in
# front of the given class.

import sqlite3 as lite
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def getClass(description,myDB):
	myclass = None
	try:
		con = None
		con = lite.connect(myDB)
		cur = con.cursor()
	# Get list of classifications
		sqlquery = "select class from classifications"
		try:
			cur.execute(sqlquery)
			classes = cur.fetchall()
		except Exception as e:
			print(e)
			classes = ""
			pass
	except Exception as e:
		print(e)
		pass
	### Guess classification for description and return value
	#		- Classes should be case/syntax insensitive (e.g., "Black Beans" = "black beans" = "black_beans")
	class_list = [x[0] for x in classes]
	try:
		extraction = process.extractOne(description, class_list)
		if extraction[1] >= 80:
			myclass = extraction[0]
	except:
		pass
	return myclass

