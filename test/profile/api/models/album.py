##################################################
# The library functions for the album database model
# This defines the required document as well as easy-to-use functions to get user information
##################################################
from api import db
#from flask.ext.login import UserMixin, AnonymousUser
#from datetime import datetime

class Album(db.Document):
    creator = db.StringField(min_length = 3, max_length = 25, required = true)
    title = db.StringField(min_length = 3, max_length = 25, required = true)
    dscrp = db.StringField(min_length = 3, max_length = 400)
    pins = db.ListField()
