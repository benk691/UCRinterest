##################################################
# The library functions for the user database model
# This defines the required document as well as easy-to-use functions to get user information
##################################################
from flask.ext.login import UserMixin, AnonymousUser

class User(UserMixin, Document):
    '''User database model. Fields:
    - uname : user name, this needs to be unique
    - fname : first name
    - lname : last name
    - email : email address
    - pwd   : password
    - img_array : array of img ids
    '''
    uname = StringField(min_length=3, max_length=25, unique=True, required=True)
    pwd = StringField(min_length=3, max_length=50, required=True)
    fname = StringField(min_length=3, max_length=25, required=True)
    lname = StringField(min_length=3, max_length=25, required=True)
    email = StringField(min_length=3, max_length=50, required=True)
    img_array = ListField()

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.uname)

class Anonymous(AnonymousUser):
    name = u"Anonymous"

