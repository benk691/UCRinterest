##################################################
# The library functions for the album database model
# This defines the required document as well as easy-to-use functions to get user information
##################################################
from ucri import db

class Album(db.Document):
    creator = db.StringField(min_length = 3, max_length = 25, required = True)
    title = db.StringField(min_length = 3, max_length = 25, required = True)
    dscrp = db.StringField(min_length = 3, max_length = 400)
    pins = db.ListField()
