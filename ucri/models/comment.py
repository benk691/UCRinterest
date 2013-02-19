##################################################
# The library functions for the comment model
# This defines the required document as well as easy-to-use functions to get user information
##################################################
from ucri import db
from user import User

class Comment(db.EmbeddedDocument):
    '''Comment is an embedded document. Fields:
    - content : the content of the comment
    - author : the author of the comment
    '''
    content = db.StingField(required=True)
    author = db.ReferenceField(required=True, reverse_delete_rule=db.DENY)
