##################################################
# The library functions for the user database model
# This defines the required document as well as easy-to-use functions to get user information
##################################################
from ucri import db
from flask.ext.login import UserMixin, AnonymousUser
from settings import *

class User(UserMixin, db.Document):
    '''User collection model. Fields:
    - uname : user name, this needs to be unique
    - fname : first name
    - lname : last name
    - email : email address
    - pwd   : password
    - pin_array : array of pin ids
    '''
    uname = db.StringField(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH, unique=True, required=True)
    fname = db.StringField(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH, required=True)
    lname = db.StringField(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH, required=True)
    gender = db.StringField(min_length=1, max_length=1, required=True)
    pwd = db.StringField(min_length=PWD_MIN_LENGTH, max_length=PWD_MAX_LENGTH, required=True)
    email = db.StringField(min_length=PWD_MIN_LENGTH, max_length=PWD_MAX_LENGTH, required=True)
    dscrp = db.StringField(min_length=DSCRPT_MIN_LENGTH, max_length=DSCRPT_MAX_LENGTH)
    creation_date = db.DateTimeField(required=True)
    birthday = db.DateTimeField()
    #pin_array = db.ListField()
    interest_array = db.ListField()

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.uname)

class Anonymous(AnonymousUser):
    uname = u"Anonymous"
