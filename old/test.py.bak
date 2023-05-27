#! /usr/bin/env python
import sqlite3 as lite 

from classificator import getClass
myDB = "/Users/aaronr/Documents/fs_raspberrypi_contents/root/home/fs/Documents/fs.db"
desc = "Del Monte Pineapple Crushed In Its Own Juice"

#sqlquery = "select description from food where classification is null"
sqlquery = "select description from food"
try:
	con = None
	con = lite.connect(myDB)
	cur = con.cursor() 
	try:
		cur.execute(sqlquery)
		descriptions = cur.fetchall()
	except Exception, e:
		print e
		descriptions = ""
		pass 
except Exception, e:
		print e

desc_list = [x[0] for x in descriptions] 

for desc in desc_list:
	if desc is not None and desc is not "" and desc is not " ":
		myvar = getClass(desc,myDB)
		print "Desc: ",desc,"Class: ",myvar

exit()
