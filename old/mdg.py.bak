#! /usr/bin/python
print('Content-type: text/html\r\n\r')

# GOAL: Take data from bitten database for moose component build times and put
# them in a pretty graph format. 
# We want a time/duration graph and a histogram-style one for the same: Week, Month, Quarter

# Try to make python at least as good as Bash
import time, os, shutil, sys, datetime, subprocess
# Try to make python better than Bash
import sqlite3 as sql            
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

# globals
today=int(time.time())
week=today-804800
month=today-3419200
quarter=today-10257600
imgdir="/srv/www/htdocs/mgraphs/img"
mytable="bitten_build"
mydb="/srv/www/htdocs/mgraphs/bs.db"
test_list=[]
test_list=["fission-gnu", "fission-intel", "quark-stable", "sandy-dynamic", "snout-gnu"]
myhome="/srv/www/htdocs/mgraphs"
os.environ[ 'HOME' ] = myhome

def update_db():
	pass
	# This doesn't work because wwwrun doesn't have read perms in Moose folder there.
	#subprocess.Popen(["/bin/bash", "/srv/www/htdocs/mgraphs/update_db.sh"])

def directory_prep():
	if os.path.exists(imgdir): shutil.rmtree(imgdir)
	if not os.path.exists(imgdir): os.makedirs(imgdir)
	os.chdir(myhome)

def data_prep():
	for test in test_list:
		for duration in "week","month","quarter":
			if "week" in duration: durs=week
			if "month" in duration: durs=month
			if "quarter" in duration: durs=quarter
			con = None
			try:
				con = sql.connect(mydb)
				sqlc = con.cursor()
				sqlst = "select * from %s where slave='%s' and status='S' and config='049AppsbecauseofMOOSE' and rev_time >= %d" % (mytable,test,durs)
				sqlc.execute(sqlst)
				sqld = sqlc.fetchall()
				# Graph linegraph
				my_linedata = []
				for line in sqld:
					my_linedata.append((line[3],(line[7]-line[6])/60.0))
				my_linedata.sort()
				graph_timeline(test+"_"+duration,"Date","Build Time (m)",my_linedata)
				# Graph histogram
				my_durations = []
				for line in sqld:
					my_durations.append((line[7]-line[6])/60)
				my_durations.sort()
				graph_histogram(test+"_"+duration,"Build Times (m)","# In Bins",my_durations)
			except sql.Error, e:
				print "Error %s:" % e.args[0]
				sys.exit(1)
			finally:
				if con:
					con.close()
		print "Graphs for "+test+" completed."

def graph_timeline(title,xaxis,yaxis,data):
	# str title, int xaxis, int yaxis, tuple data(int, int)
	hfmt = mpl.dates.DateFormatter('%m/%d %H:%M')
	figure = plt.figure()
	fig = figure.add_subplot(111)
	x = [tup[0] for tup in data]
	y = [tup[1] for tup in data]
	#dates=[datetime.datetime.fromtimestamp(ts,est) for ts in y]
	#x = data[:,1]
	#y = data[:,0]
	fig.plot(x, y, marker='o', linestyle=' ', color='blue')
	fig.set_xlabel(xaxis)
	fig.set_ylabel(yaxis)
	fig.set_title(title)
	x_min = int(min(x)-10)
	x_max = int(max(x)+10)
	y_min = 0
	y_max = int(max(y)+10)
	fig.axis([x_min, x_max, y_min, y_max])
	#fig.xaxis.set_major_formatter(hfmt)
	#plt.xticks(rotation='vertical')
	fig.grid(True)
	figure.savefig(imgdir+"/"+title+'.png',dpi=96)

def graph_histogram(title,xaxis,yaxis,data):
	# str title, int xaxis, int yaxis, list data(int)
	figure = plt.figure()
	fig = figure.add_subplot(111)
	x = data
	n, bins, patches = plt.hist(x, 15, facecolor='orange', alpha=0.75)
	# add a 'best fit' line
	# Got mu, not sure how to compute sigma
	#mu = x[len(x)/2]
	#npx = np.array(x)
	#sigma = npx.std()
	#y = mlab.normpdf( bins, mu, sigma)
	#l = plt.plot(bins, y+10, 'r--', linewidth=1)
	fig.set_xlabel(xaxis)
	fig.set_ylabel(yaxis)
	fig.set_title(title)
	axis_low = int(x[0]-10)
	axis_high = int(x[-1:][0]+10)
	max_num = len(x)/1.5
	fig.axis([axis_low, axis_high, 0, max_num])
	fig.grid(True)
	figure.savefig(imgdir+"/"+title+'_hist.png',dpi=96)
		
if __name__=="__main__":
	update_db()
	directory_prep()
	data_prep()
	print '<meta http-equiv="REFRESH" content="0;url=http://hpcsc.inl.gov/mgraphs">'	

