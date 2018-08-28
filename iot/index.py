import webapp2
import os
import time
import datetime
import random
import json
import sqlite3
import jinja2
import pytz

conn = sqlite3.connect('/var/www/iot/telem.db', check_same_thread=False)
c = conn.cursor()

def create_table():
  c.execute("CREATE TABLE IF NOT EXISTS Location(Location TEXT, Time TEXT)")


#def data_update(Id,State):
#  c.execute("UPDATE iot SET Id = ?, State = ? WHERE Id = ?",(Id, State, Id))
#  conn.commit()

def data_entry(Location):
  Time = datetime.datetime.now()
  c.execute("INSERT INTO Location(Location, Time) VALUES(?, ?)",(str(Location), str(Time)))
  conn.commit()

create_table()

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
    self.render("index.html")
  def post(self):
   # self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
    Location = self.request.get("Location")
    data_entry(Location)
#    self.redirect('/view')


class query(handler):
  def get(self):
   # Id = self.request.get("Id")
    c.execute("SELECT * FROM Location")
    #datas = c.fetchall()
    rows = [x for x in c.fetchall()]
    cols = [x[0] for x in c.description]
    songs = []
    for row in rows:
      song = {}
      for prop, val in zip(cols, row):
        song[prop] = val
      songs.append(song)
    self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
    self.response.write(json.dumps(songs))
    #else:
     # error = "Please Give any bin number"
     # self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
     # self.response.write(json.dumps(

application = webapp2.WSGIApplication([
    ('/', Hello),('/query', query)
], debug=True)
