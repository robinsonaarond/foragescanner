#!/usr/bin/python2 -W ignore
# -*- encoding: latin-1 -*-
import sys, urllib, time
sys.path.append(r'/home/fs/test_code/npyscreen-2.0pre68')
import npyscreen
import curses as curses
import sqlite3 as lite
import socket

# Globals
myQuantity = 1
myAmount = 0
myDB = "/home/fs/Documents/fs.db"
ar = "ADD"
desc = False
last_updated=str(time.strftime("%m-%d-%Y", time.gmtime()))

class MyApplication(npyscreen.NPSAppManaged):
	def onStart(self):
		self.addForm("MAIN", MainMenu, name='Forage Scanning System', minimum_lines=10, minimum_columns=10)
		self.addForm("ADD", AddScreen, name='Adding Item(s)...', minimum_lines=10, minimum_columns=10)
		self.addForm("REMOVE", RemoveScreen, name='Removing Item(s)...', minimum_lines=10, minimum_columns=10)
		self.addForm("DBEDIT", DBEdit, name='Forage Database', minimum_lines=10, minimum_columns=10)
	def changeForm(self, name):
		self.switchForm(name)
		self.resetHistory()

class MainMenu(npyscreen.FormBaseNew):
	def create(self):
		self.add(menuButtonOne, name="Add item(s)...")
		#self.add(menuButtonTwo, name="Remove item(s)...")
		self.add(menuButtonDB, name="View/Edit Database")
		self.add(menuButtonExit, name="Exit")

class AddScreen(npyscreen.FormBaseNew):
	def create(self):
		actionstring = "UPC"
		self.UpdateBy = self.add(npyscreen.FixedText, value="Enter "+str(actionstring)+" below:", editable=False)
		self.UPCInput = self.add(OmniBox, name=' ')
		self.DisplayBanner = self.add(npyscreen.FixedText, value="----", editable=False)
		self.add(npyscreen.FixedText, editable=False)
		self.add(npyscreen.FixedText, editable=False)
		self.DisplayQuantity = self.add(npyscreen.FixedText, value="Quantity: "+str(myQuantity), editable=False)
		self.DisplayAmount = self.add(npyscreen.FixedText, value="  Amount: "+str(myAmount), editable=False)
		self.add(npyscreen.FixedText, editable=False)
		self.add(menuButtonMain, name="Main Menu")
		

class RemoveScreen(AddScreen):
	pass

class DBEdit(npyscreen.FormBaseNew):
	placeholder = "true"
	def create(self):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect(("gmail.com",80))
			ipaddr=str(s.getsockname()[0])
			s.close()
		except:
			ipaddr="<none found>"
		self.add(npyscreen.FixedText, value="Please go to another comp-", editable=False)
		self.add(npyscreen.FixedText, value="uter connected to the same", editable=False)
		self.add(npyscreen.FixedText, value="network as the Forage sys-", editable=False)
		self.add(npyscreen.FixedText, value="tem and open an Internet", editable=False)
		self.add(npyscreen.FixedText, value="Browser, then navigate to", editable=False)
		self.add(npyscreen.FixedText, value="http://"+ipaddr+" to", editable=False)
		self.add(npyscreen.FixedText, value="access the database.", editable=False)
		self.add(npyscreen.FixedText, value="", editable=False)
		self.add(menuButtonMain, name="Main Menu")

class menuButtonOne(npyscreen.MiniButtonPress):
	def whenPressed(self):
		self.parent.parentApp.changeForm("ADD")

class menuButtonTwo(npyscreen.MiniButtonPress):
	def whenPressed(self):
		self.parent.parentApp.changeForm("REMOVE")

class menuButtonDB(npyscreen.MiniButtonPress):
	def whenPressed(self):
		self.parent.parentApp.changeForm("DBEDIT")

class menuButtonMain(npyscreen.MiniButtonPress):
	def whenPressed(self):
		self.parent.parentApp.changeForm("MAIN")

class menuButtonExit(npyscreen.MiniButtonPress):
	def whenPressed(self):
		self.parent.parentApp.changeForm(None)

class OmniBox(npyscreen.Textfield):
	def set_up_handlers(self):
		super(OmniBox, self).set_up_handlers()
		self.handlers.update ({
			curses.ascii.NL:    self.OmniBox_Input,
			curses.ascii.CR:    self.OmniBox_Input,
		})
	def OmniBox_Input(self, myargs):
		if desc == False:
			try:
				# Process UPC
				if int(self.value) >= 9999:
					myUPC = str(self.value)
					self.value = ""
					# Get description for this UPC from DB/Online
					try:
						# Open database
						con = None
						con = lite.connect(myDB)
						cur = con.cursor()
						sqlquery = "select description from food where upc=?"
						try:
							# Look for UPC
							cur.execute(sqlquery, [(myUPC)])
							fetched = cur.fetchone()
							if type(fetched) is tuple:
								# Get description from database
								upcdesc = fetched[0]
							else:
								# Get it from Online
								myURL = "http://www.upcdatabase.com/item/"+str(myUPC)
								urlpage = urllib.urlopen(myURL)
								urlpage = urlpage.readlines()
								upcdesc = [ l for l in urlpage if "Description" in l ]
								if not upcdesc:
									# If description is empty, get it from user
									# I have to call the Omnibox again. Kind of messy...
									#upcdesc = raw_input("Please enter desc. above.")
									global desc
									desc = True
									#self.parent.DisplayBanner.value = str(myUPC)
									self.parent.DisplayBanner.value = "Hello"
									self.parent.UpdateBy.value = "Enter desc. for "+str(myUPC)+":"
									self.value = ""
									global gUPC
									gUPC = myUPC
									#self.parent.exit_editing()
									self.parent.parentApp.changeForm(ar)
								else:
									# Get first result (there should only be one), strip, and convert to string.
									upcdesc = str(upcdesc[0]).replace("<tr><td>Description</td><td></td><td>","").replace("</td></tr>","").rstrip('\n')
						except Exception, e:
							self.parent.DisplayBanner.value = "Could not get description!"
							self.parent.exit_editing()	
							upcdesc = "No Desc."+str(e)
					except:
						self.parent.DisplayBanner.value = "Database access error."
						self.parent.exit_editing()	
					try:
						global myAmount
						# Initialize DB
						con = None
						con = lite.connect(myDB)
						cur = con.cursor()
						# Get amount from DB
						sqlquery = "select amount from food where upc=?"
						try:
							cur.execute(sqlquery, [(myUPC)])
							fetched = cur.fetchone()
							if type(fetched) is tuple:
								global myAmount
								myAmount = fetched[0]
							else:
								#Add to database
								global myAmount
								myAmount = 0
								sqlquery = "insert into food(upc, amount, description, lastupdated) values(?,?,?,?)"
								sqlargs = (myUPC, myAmount, upcdesc, last_updated)
								cur.execute(sqlquery, sqlargs)
								con.commit()
						except:
							myAmount = 0
						# Add/Remove from amount
						if ar == "ADD":
							myAmount = myAmount + myQuantity
						if ar == "REMOVE":
							myAmount = myAmount - myQuantity
						cur.execute("update food set amount=? where upc=?",(myAmount,myUPC))
						con.commit()
					except lite.Error, e:
						self.parent.DisplayBanner.value = "Database access error."
						self.parent.exit_editing()	
	
					# Update Description, Amount, Quantity	
					self.parent.DisplayBanner.value = upcdesc+"            "+str(type(upcdesc))
					self.parent.DisplayAmount.value = "  Amount: "+str(myAmount)
					global myQuantity
					myQuantity = 1
					self.parent.DisplayQuantity.value = "Quantity: "+str(myQuantity)
					self.parent.exit_editing()	
				# Must be quantity update
				else:
					#global myQuantity
					myQuantity = int(self.value)
					self.value = ""
					self.parent.DisplayBanner.value = "(Quantity updated.)"
					self.parent.exit_editing()
					self.parent.DisplayQuantity.value = "Quantity: "+str(myQuantity)
			except Exception,e:
				# Must be text, and we weren't asking for a description
				# Was it the add/remove?
				if self.value in ("Add", "add", "a", "A", "+"):
					self.value = ""
					global ar
					self.parent.parentApp.changeForm("ADD")
					ar = "ADD"
				elif self.value in ("Remove", "remove", "rem", "Rem", "r", "R", "-"):
					self.value = ""
					global ar
					self.parent.parentApp.changeForm("REMOVE")
					ar = "REMOVE"
				else:
					if self.parent.DisplayBanner.value == "Hello":
						self.parent.DisplayBanner.value = "----"
					else:
						self.parent.DisplayBanner.value = "(Invalid UPC/Amount)    "+str(e)+"."
					self.value = ""
					self.parent.exit_editing()
		else:
			# Getting the description, then perform all the work.  I have to put it twice until I figure out how to make it into a function
			global desc
			desc = False
			upcdesc = self.value
			myUPC = gUPC
			try:
				global myAmount
				# Initialize DB
				con = None
				con = lite.connect(myDB)
				cur = con.cursor()
				# Get amount from DB
				sqlquery = "select amount from food where upc=?"
				try:
					cur.execute(sqlquery, [(myUPC)])
					fetched = cur.fetchone()
					if type(fetched) is tuple:
						global myAmount
						myAmount = fetched[0]
					else:
						#Add to database
						global myAmount
						myAmount = 0
						sqlquery = "insert into food(upc, amount, description, lastupdated) values(?,?,?,?)"
						sqlargs = (myUPC, myAmount, upcdesc, last_updated)
						cur.execute(sqlquery, sqlargs)
						con.commit()
				except:
					myAmount = 0
				# Add/Remove from amount
				if ar == "ADD":
					myAmount = myAmount + myQuantity
				if ar == "REMOVE":
					myAmount = myAmount - myQuantity
				cur.execute("update food set amount=? where upc=?",(myAmount,myUPC))
				con.commit()
			except lite.Error, e:
				self.parent.DisplayBanner.value = "Database access error."
				self.parent.exit_editing()
				
			# Update Description, Amount, Quantity  
			self.parent.DisplayBanner.value = upcdesc+str(type(upcdesc))
			self.parent.DisplayAmount.value = "  Amount: "+str(myAmount)
			global myQuantity
			myQuantity = 1
			self.parent.DisplayQuantity.value = "Quantity: "+str(myQuantity)

			# Update everything else
			self.parent.DisplayBanner.value = str(self.value)+"            "
			self.value = ""
			self.parent.UpdateBy.value = "Enter UPC Below:"
			self.parent.exit_editing()
	
if __name__ == '__main__':
	TestApp = MyApplication().run()
