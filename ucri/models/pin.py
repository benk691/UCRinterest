##################################################
# The library functions for the pin database model
# This defines the required document as well as easy-to-use functions to get user information
##################################################
from ucri import db
from settings import *

class Pin(db.Document):
    '''Pin collection model. Fields:
    - title : title of the pin
    - dscrp : description
    - date : date format
    - orig : original [t/f]
    - cat : category
    - img : image
    '''
    title = db.StringField(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH, required=True)
    dscrp = db.StringField(min_length=DSCRPT_MIN_LENGTH, max_length=DSCRPT_MAX_LENGTH)
    orig = db.BooleanField() # Not sure about this field
    date = db.DateTimeField()
    img = db.ImageField(required=True)
