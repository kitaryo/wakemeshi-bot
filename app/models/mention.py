from google.appengine.ext import db

class Mention(db.Model):
  id = db.IntegerProperty()
  date = db.DateTimeProperty(auto_now_add=True)
