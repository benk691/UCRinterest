##################################################
# The library functions for the user database model
# This defines the required document as well as easy-to-use functions to get user information
##################################################
from flask.ext.login import UserMixin, AnonymousUser, current_user
from ucri import db
from settings import *
from notification import Notification

class User(UserMixin, db.Document):
    '''User collection model. Fields:
    - uname : user name, this needs to be unique
    - fname : first name
    - lname : last name
    - email : email address
    - pwd   : password
    - pin_array : array of pin ids
    - interest_array : array of interests
    '''
    uname = db.StringField(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH, unique=True, required=True)
    fname = db.StringField(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH, required=True)
    lname = db.StringField(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH, required=True)
    img = db.StringField(min_length=PATH_MIN_LENGTH, required=True)
    gender = db.StringField(min_length=1, max_length=1, required=True)
    pin_browsers = db.StringField(min_length=1, max_length=1, required=True)
    pin_commenters = db.StringField(min_length=1, max_length=1, required=True)
    pwd = db.StringField(min_length=PWD_MIN_LENGTH, max_length=PWD_MAX_LENGTH, required=True)
    email = db.EmailField(min_length=PWD_MIN_LENGTH, max_length=PWD_MAX_LENGTH, required=True)
    dscrp = db.StringField(min_length=DSCRPT_MIN_LENGTH, max_length=DSCRPT_MAX_LENGTH)
    creation_date = db.DateTimeField(required=True)
    bday = db.DateTimeField(required=True)
    interest_array = db.ListField()
    notification_array = db.ListField(db.EmbeddedDocumentField(Notification))
    follower_array = db.ListField(db.ReferenceField('self', reverse_delete_rule=db.PULL, dbref=True))
    repins_from = db.ListField(db.ReferenceField('self', dbref=True))
    meta = { 'category' : 'user' }

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.uname)

    #Tests if current_user is following this User
    def following(self):
        for user in current_user.follower_array:
            if user == self:
                return True
        else:
            return False

class Anonymous(AnonymousUser):
    uname = u"Anonymous"

    def is_active(self):
        return False
