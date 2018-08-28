import webapp2
import os
import time
import datetime
import random
import json
import sqlite3
import jinja2

conn = sqlite3.connect('/var/www/veg/Veg_Table.db', check_same_thread=False)
c = conn.cursor()
price = 0

def create_table():
  c.execute("CREATE TABLE IF NOT EXISTS veg(Id TEXT, Veg TEXT,Image TEXT,Price_Half TEXT,Price_One TEXT,Price_Two TEXT)")


def update_table(Price_Half, Price_One, Price_Two, Offer):
  for i in range(0,66):
  	c.execute("UPDATE veg SET Price_Half = ?, Price_One = ?, Price_Two = ?, Offer = ?  WHERE Id = ? ",(Price_Half[i], Price_One[i], Price_Two[i], Offer[i], i))
  conn.commit()


create_table()

veg =['ash Gourd - Parangikai','Brinjal - kathirikai', 'Baby corn', 'Beetroot', 'Bottle Gourd - Sorakai',
 'Bitter Gourd - Pakarkai', 'cabbage - Muttakoose', 'Capsicum - kudaimilakai', 'Califlower', 
 'cluster beans - kothavarangai', 'Coconut - thengai', 'Coriander leaves - kothamalli', 'Corn',
  'Cucumber - velrikai', 'Curry Leaves - karuvepilai', 'DrumStick - Murungaikai', 'French Bean',
   'Garlic - poondu', 'Ginger - Enji', 'Green chilli', 'Lemon ', 'Mushroom - Kaalan', 'Small Onion - chinna vengayam',
    'Big onion - Prtiya vengayam', 'Ladies Finger - Vendaikai', ' Peas - Pattani', 'Mint Leaves - Pudina', 'Pumbkin - Poosanikai', 
    'Potato - Urulai kilangu', 'Radish - Mullangi', 'Raw Banana - Valakai', 'Red chilli - Varamilakai', 'Sweet Potato - Chakaravallikelangu', 
    'Tomato - Thakkali', 'Hybrid tomato - Hybrid thakali', 'Yam - Senaikelangu', 'Ridge Gourd - peerkangai', 'chow chow - seemai kathirikai',
     'Ground nut - Nilakadalai', 'Bitter Gourd forest - chinna bavakai', 'Broccoli', 'Turmaric - manjal', 'Banana Stem - valathandu', 'Carrot', 
     'Tapiacco - Maravallikelangu', 'kovakai', 'Snake Gourd - Podalangai', 'Lettuce - Ellaikose', 'Turnip - kosekilangu', 'Murungai keerai', 
     'Vendaya Keerai', 'Pulicha keerai', 'Moolai keerai', 'Thandu keerai', 'Ara keerai', 'Seru keerai', 'Ponankanni Keerai', 'Poloi keerai',
      'Agathu keerai', 'Karisalangani keerai', 'Parupa Keerai', 'Mani thakali Keerai', 'Vellarai keerai', 'Thooduvalai', 'Perandai', 'mangosteen']

template_dir=os.path.join(os.path.dirname(__file__))
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),autoescape=True)


class handler(webapp2.RequestHandler):
  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)
  
  def render_str(self, template, **params):
    t=jinja_env.get_template(template)
    return t.render(params)
  
  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))

class Hello(handler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
    c.execute("SELECT * FROM veg")
    Data = c.fetchall()
    conn.commit()
    self.render("index.html", datas = Data)
  def post(self):
    Price_Half = []
    Price_One = []
    Price_Two = []
    Offer = []
    for i in range(0,66):
      Price_Half.append(self.request.get("Price_Half"+str(i)))
      Price_One.append(self.request.get("Price_One"+str(i)))
      Price_Two.append(self.request.get("Price_Two"+str(i)))
      Offer.append(self.request.get("Offer"+str(i)))
    update_table(Price_Half, Price_One, Price_Two, Offer)
    self.redirect("/")

class data(handler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
    c.execute("SELECT * FROM veg")
    Data = c.fetchall()
    conn.commit()
    self.write(json.dumps(Data))

		

application = webapp2.WSGIApplication([
    ('/', Hello),
    ('/json', data),
], debug=True)


