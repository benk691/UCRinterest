##################################################
# The library functions for the pin database model
# This defines the required document as well as easy-to-use functions to get user information
##################################################
from ucri.UCRinterest.ucri import db

class Pin(db.Document):
    '''Pin collection model. Fields:
    - title : title of the pin
    - dscrp : description
    - date : date format
    - orig : original [t/f]
    - cat : category
    - img : image
    '''
    title = db.StringField(min_length=3, max_length=25, required=True)
    dscrp = db.StringField(min_length=1, max_length=400)
    orig = db.StringField(min_length=1, max_length=1) # Not sure about this field
    date = db.DateTimeField()
    img = db.ImageField(required=True)
