import datetime
from google.appengine.ext import db
from google.appengine.api import users

class User(db.Model):
	account = db.UserProperty()
	join_date = db.DateProperty()

class Project(db.Model):
	tag = db.StringProperty(required=True)
	name = db.TextProperty(required=True)
	description = db.BlobProperty()
	creator = db.UserProperty(required=True)

class UserMemberships(db.Model):
	user = db.UserProperty(required=True)
	project = db.ReferenceProperty(Project, required=True)