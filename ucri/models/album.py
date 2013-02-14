##################################################
# The library functions for the album database model
# This defines the required document as well as easy-to-use functions to get user information
##################################################
from ucri import db
from settings import *

class Album(db.Document):
    '''Album object:
    creator - creator of album 
    title - title of album
    dscrp - description of album
    pins - pins attached to album
    '''
    creator = db.StringField(min_length = NAME_MIN_LENGTH, max_length = NAME_MAX_LENGTH, required = True)
    title = db.StringField(min_length = NAME_MIN_LENGTH, max_length = NAME_MAX_LENGTH, required = True)
    dscrp = db.StringField(min_length = DSCRPT_MIN_LENGTH, max_length = DSCRPT_MAX_LENGTH)
    pins = db.ListField()
