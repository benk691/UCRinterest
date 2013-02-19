##################################################
# The library functions for the pin database model
# This defines the required document as well as easy-to-use functions to get user information
##################################################
from ucri import db
from settings import *
from user import User

class Pin(db.Document):
    '''Pin collection model. Fields:
    - title : title of the pin
    - dscrp : description
    - date : date format
    - orig : original [t/f]
    - cat : category
    - img : image
    - cmts : a list of comments
    '''
    title = db.StringField(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH, required=True)
    #img = db.ImageField(required=True)
    img_path = db.StringField(required=True, min_length=PATH_MIN_LENGTH)
    pinner = db.ReferenceField(User, required=True, reverse_delete_rule=db.DENY)
    dscrp = db.StringField(min_length=DSCRPT_MIN_LENGTH, max_length=DSCRPT_MAX_LENGTH)
    orig = db.BooleanField(default=False)
    date = db.DateTimeField(required=True)
    cmts = db.ListField()
    meta = { 'category' : 'img' }
