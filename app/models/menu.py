from google.appengine.ext import db

class Menu(db.Model):
    date = db.DateProperty(required=True)
    menu = db.StringListProperty()
    last_update = db.DateProperty()
