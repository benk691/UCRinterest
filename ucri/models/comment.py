##################################################
# The library functions for the comment model
# This defines the required document as well as easy-to-use functions to get user information
##################################################
from ucri import db
from settings import *
from user import User

class Comment(db.EmbeddedDocument):
    '''Comment is an embedded document. Fields:
    - content : the content of the comment
    - author : the author of the comment
    '''
    commenter = db.ReferenceField(User, dbref=True, required=True)
    message = db.StringField(min_length=DSCRPT_MIN_LENGTH+1, max_length=DSCRPT_MAX_LENGTH, required=True)
    date = db.DateTimeField(required=True)
