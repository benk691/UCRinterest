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
    content = db.StringField(required=True, min_length=CMT_MIN_LENGTH)
    # author is the uname in the User model
    author = db.StringField(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH, required=True)
