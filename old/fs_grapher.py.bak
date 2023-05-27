#! /usr/bin/python2

# Try to make python at least as good as Bash
import time, os, shutil, sys, datetime, subprocess
# Try to make python better than Bash
import sqlite3 as sql            
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# globals
imgdir="/srv/http/img"
mydb="/home/fs/Documents/fs.db"
myhome="/srv/http"
os.environ[ 'HOME' ] = myhome

def main_prep():
	con = None
	try:
		con = sql.connect(mydb)
		sqlc = con.cursor()
		sqlst = "select * from %s" % ("classifications",)
		sqlc.execute(sqlst)
		sqld = sqlc.fetchall()
		my_linedata = []
		for line in sqld:
			sqlst = "select sum(amount) from food where classification like '%s'" % (line[0],)
			sqlc.execute(sqlst)
			myAmount = sqlc.fetchone()
			if myAmount[0] is None:
				par_amount = 0
			else:
				par_amount = myAmount[0]
			# Comes out classification, par, current percentage.
			#my_linedata.append((str(line[0])+"("+str(line[1])+")",(100.0*float(myAmount[0])/float(line[1]))))
			#print "line[0]",line[0],"myAmount[0]",myAmount[0],"line[1]",line[1],"par_amount",par_amount
			my_linedata.append((str(line[0])+"("+str(line[1])+")",(100.0*float(par_amount)/float(line[1])),myAmount[0]))
		my_linedata.sort()
		#print my_linedata
		graph_timeline("Par Percentages","Classifications","Percentage",my_linedata)
	except sql.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)
	finally:
		if con:
			con.close()

def autolabel(rects,hmax,data):
	# attach some text labels
	i=0
	for rect in rects:
		height = rect.get_height()
		if height > hmax:
			myheight = hmax + 1
		else:
			myheight = height
		#plt.text(rect.get_x()+rect.get_width()/2., 1.05*myheight, '%d'%int(height), ha='center', va='bottom', fontsize=7)
		if data[i][2] is None:
			current_amount = 0
		else:
			current_amount = data[i][2]
		plt.text(rect.get_x()+rect.get_width()/2., 1.05*myheight, '%d'%current_amount, ha='center', va='bottom', fontsize=7)
		i+=1

def graph_timeline(title,xaxis,yaxis,data):
	# title, xaxis, yaxis, data(str(classification), int(par), int(current))
	figure = plt.figure(num=None, figsize=(25, 4.75), dpi=80)
	fig = figure.add_subplot(111)
	#x = [tup[0] for tup in data]
	y = [tup[1] for tup in data]
	ind = range(len(y))
   	fig.set_ylabel(yaxis)
	fig.set_xlabel(xaxis)
   	x_min = 0
	x_max = len(y)
   	y_min = 0
	y_max = 110
	fig.axis([x_min, x_max, y_min, y_max])
	fig.set_title(title)
	fig.set_xticks(ind)
	classes = [tup[0] for tup in data]
	fig.set_xticklabels(classes)
	plt.xticks(rotation='75', fontsize='9')
	plt.axhline(y=100, linewidth=2, color='r', linestyle="dotted")
	plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
	colors = []
	#print data
	#exit()
	#colors = ['red','orange','yellow','blue']
	for percent in data:
		if 0.0 <= percent[1] <= 24.9:
			colors.append('red')
		elif 25.0 <= percent[1] <= 49.9:
			colors.append('orange')
		elif 50.0 <= percent[1] <= 74.9:
			colors.append('yellow')
		elif 75.0 <= percent[1] <= 100000.0:
			colors.append('blue')
	
	mybars = fig.bar(ind, y, width=.9, color=colors)
	#mybars = fig.bar(ind, y, facecolor="#3322FF", width=.9, color=colors)
	autolabel(mybars,y_max,data)
	#fig.grid(True)
	figure.savefig(imgdir+"/par_percentages.png", bbox_inches='tight')

if __name__=="__main__":
	main_prep()
