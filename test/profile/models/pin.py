##################################################
# The library functions for the user database model
# This defines the required document as well as easy-to-use functions to get user information
##################################################
from flask.ext.login import UserMixin, AnonymousUser
from datetime import datetime

class Pin(Document):
    '''Pin collection model. Fields:
    - title : title of the pin
    - dscrp : description
    - date : date format
    - orig : original [t/f]
    - cat : category
    - img : image
    '''
    title = StringField(min_length=3, max_length=25, required=True)
    email = StringField(min_length=3, max_length=50, required=True)
    dscrp = StringField(min_length=1, max_length=400)
    orig = StringField(min_length=1, max_length=1) # Not sure about this field
    date = DateTimeField()
    img = ImageField(required=True)
