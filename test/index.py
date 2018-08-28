import os
import webapp2
import jinja2
import sqlite3
import datetime
from datetime import timedelta,date
import json
import smtplib
import pymysql
from collections import defaultdict


conn = pymysql.connect(
    db='dream',
    user='root',
    passwd='shanave',
    host='localhost')


template_dir=os.path.join(os.path.dirname(__file__),'web')
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),autoescape=True)

def data_entry(Hotel, Name, Mail, Phone, Room, Arrival, Depature):
	c = conn.cursor()
	c.execute("INSERT INTO Booking (Hotel, Name, Mail, Phone, Room, Arrival, Depature) VALUES (%s, %s, %s, %s, %s, %s, %s)",(Hotel, Name, Mail, Phone, Room, Arrival, Depature))
	conn.commit()
	conn.close()
	c.close()

def data_entry_status(Hotel, Room, Datee, Status):
	c = conn.cursor()
	Created = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	c.execute("INSERT INTO Status (Hotel, Room, Datee, Created, Status) VALUES (%s, %s, %s, %s, %s)",(Hotel, Room, Datee, Created, Status))
	conn.commit()
	conn.close()
	c.close()

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

class handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
		t=jinja_env.get_template(template)
		return t.render(params)
    def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainPage(handler):
	def get(self):
		self.render("index.html")

	def post(self):
		hotel = self.request.get("Hotel")
		self.redirect("/%s"%hotel)

class Admin(handler):
	data = {}
	data["LeCastle"] = {"budgetromantic":1,"romantic":12,"quadratic":7,"nuclear":2,"star":1,"banquet":1,"dormitory":1}
	data["BlueStar"] = {"cottage":2}
	data["Madhu"] = {"romantic":5,"quadratic":3,"nuclear":5,"banquet":1}
	data["Prince"] = {"cottage":3}
	def get(self):
		self.render("admin.html")
	def post(self):
		self.render("admin.html",d=myDict)			



class LeCastle(handler):
	def renderform(self):
		self.render("rooms.html")

	def get(self):
		self.renderform();


		
class MadhuResidency(handler):
	def renderform(self):
		self.render("madhu.html")
		
	def get(self):
		self.renderform();

		
class PrinceCottage(handler):
	def renderform(self):
		self.render("prince.html")
		
	def get(self):
		self.renderform();


class BlueStar(handler):
	def renderform(self):
		self.render("blue.html")
		
	def get(self):
		self.renderform();


class Booking(handler):
	data = {}
	data["LeCastle"] = {"budgetromantic":1,"romantic":12,"quadratic":7,"nuclear":2,"star":1,"banquet":1,"dormitory":1}
	data["BlueStar"] = {"cottage":2}
	data["Madhu"] = {"romantic":5,"quadratic":3,"nuclear":5,"banquet":1}
	data["Prince"] = {"cottage":3}
	def renderform(self, error = "", Name = "", Mail = "", Phone = "", Arrival = "", Depature = "",dates = "",Hotel = ""):
		c = conn.cursor()
		data = self.data
		myDict = defaultdict(dict)
		for i in data:
			for i, val in data.iteritems():
				for val, da in data[i].iteritems():
					c.execute(" SELECT Datee FROM Status WHERE Room = %s AND Status = %s AND Hotel = %s ",(val, da, i, ))
					myDict["%s"%i]["%s"%val] = [str(x[0]) for x in c.fetchall()]
		conn.close()
		c.close()
		self.render("reservation.html",error = error, dates = json.dumps(myDict), Name = Name, Mail = Mail, Phone = Phone, Arrival = Arrival, Depature = Depature,Hotel = Hotel)

	def get(self):
		self.renderform()

	def post(self):
		data = self.data
		Hotel = self.request.get("hotel")
		Name = self.request.get("name")
		Mail = self.request.get("mail")
		Number = self.request.get("number")
		Adults = self.request.get("adults")
		Children = self.request.get("children")
		Room = self.request.get("rooms")
		Arrival = self.request.get("arrival")
		Depature = self.request.get("depature")
		if Hotel and Name and Number and Room and Arrival and Depature:
			data_entry(Hotel,Name,Mail,Number,Room,Arrival,Depature)
			start = map(int, Arrival.split("/"))
			start_day = date(start[2],start[0],start[1])
			end = map(int ,Depature.split("/"))
			end_day = date(end[2],end[0],end[1])
			dates = [single_date.strftime("%Y-%m-%d") for single_date in daterange(start_day, end_day)]
			for i in dates:
				c = conn.cursor()
				c.execute("""SELECT Status FROM Status WHERE Hotel = %s AND Room = %s AND Datee = %s ORDER BY Created DESC LIMIT 1""",(Hotel, Room, i))
				status = c.fetchall()
				conn.close()
				c.close()
				print status
				if status:
					if int(status[0][0]) == data[Hotel][Room]:
						error = "%s,%s,%s,%s,%s,%s,%s -- ststus full"%(Hotel,Name,Mail,Number,Arrival,Depature,status)
						self.renderform(error = error, Name = Name, Mail = Mail, Phone = Number,Hotel = Hotel)
						return None
					else:
						error = "%s,%s,%s,%s,%s,%s,%s -- putdata"%(Hotel,Name,Mail,Number,dates,Depature,status)
						self.renderform(error = error)
						data_entry_status(Hotel,Room,i,(int(status[0][0])+1))
				else:
					error = "%s,%s,%s,%s,%s,%s,%s,%s -- nothing in status"%(Hotel,Name,Mail,Number,dates,Depature,status,Room)
					self.renderform(error = error)
					data_entry_status(Hotel,Room,i,1)
					
		else:
			error = "%s,%s,%s,%s,%s,%s,%s -- something important not in the status"%(Hotel,Name,Mail,Number,Arrival,Depature,Room)
			self.renderform(error=error, Name = Name, Mail = Mail, Phone = Number, Arrival = Arrival, Depature = Depature, Hotel = Hotel)


class Contact(handler):
	def get(self):
		self.render("contact.html")
	def post(self):
		User = self.request.get('userName')
		Mail = self.request.get('userEmail')
		Phone = self.request.get('userPhone')
		Msg = self.request.get('userMsg')
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login("theedush@gmail.com", "1234%5$#@!")
		msg = User+'\n'+Mail+'\n'+Phone+'\n'+Msg+'\n'
		server.sendmail("theedush@gmail.com", "createdworkmail@gmail.com", msg)
		server.quit()


class Services(handler):
	def get(self):
		self.render("activities.html")

class Packages(handler):
	def get(self):
		self.render("package.html")

class Privacy(handler):
	def get(self):
		self.render("privacy.html")

class Refund(handler):
	def get(self):
		self.render("refund.html")
	
class Terms(handler):
	def get(self):
		self.render("terms.html")
						
		

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/lecastle', LeCastle),
    ('/bluestar', BlueStar),
    ('/madhu', MadhuResidency),
    ('/prince', PrinceCottage),
    ('/booking', Booking),
    ('/contact', Contact),
    ('/services', Services),
    ('/packages', Packages),
    ('/refund', Refund),
    ('/terms', Terms),
    ('/privacy', Privacy),
    ('/admin' , Admin),
		], debug=True)
