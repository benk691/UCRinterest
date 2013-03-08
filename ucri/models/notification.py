##################################################
# The library functions for the notification model
# This defines the required document as well as easy-to-use functions to get user information
##################################################
from ucri import db
from settings import *

##########
# TODO:
#   - add an action decorator for actions that make a notification
##########

class Notification(db.EmbeddedDocument):
    '''Notification is an embedded document. Fields:
    - notifier : the user name that the notification came from
    - msg : the notifcation message
    - date : the date the notification occured
    '''
    notifier = db.StringField(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH, required=True)
    msg = db.StringField(min_length=DSCRPT_MIN_LENGTH+1, max_length=DSCRPT_MAX_LENGTH, required=True)
    date = db.DateTimeField(required=True)
