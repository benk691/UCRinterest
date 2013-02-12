##################################################
# The library functions for the user database model
# This defines the required document as well as easy-to-use functions to get user information
##################################################
from flask.ext.login import UserMixin, AnonymousUser
from datetime import datetime

class User(UserMixin, Document):
    '''User collection model. Fields:
    - uname : user name, this needs to be unique
    - fname : first name
    - lname : last name
    - email : email address
    - pwd   : password
    - pin_array : array of pin ids
    '''
    uname = StringField(min_length=3, max_length=25, unique=True, required=True)
    fname = StringField(min_length=3, max_length=25, required=True)
    lname = StringField(min_length=3, max_length=25, required=True)
    gender = StringField(min_length=1, max_length=1, required=True)
    pwd = StringField(min_length=3, max_length=50, required=True)
    email = StringField(min_length=3, max_length=50, required=True)
    dscrp = StringField(min_length=1, max_length=400)
    creation_date = DateTimeField(required=True)
    birthday = DateTimeField()
    pin_array = ListField()

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.uname)

class Anonymous(AnonymousUser):
    name = u"Anonymous"
