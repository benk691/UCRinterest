##################################################
# The library functions for the pin database model
# This defines the required document as well as easy-to-use functions to get user information
##################################################
from ucri import db
from settings import *
from user import User
from comment import Comment
from flask.ext.login import current_user

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
    img = db.StringField(required=True)
    pinner = db.ReferenceField(User, dbref=True, required=True)
    dscrp = db.StringField(min_length=DSCRPT_MIN_LENGTH, max_length=DSCRPT_MAX_LENGTH)
    orig = db.BooleanField(default=False)
    date = db.DateTimeField(required=True)
    cmts = db.ListField(db.EmbeddedDocumentField(Comment))
    repins = db.IntField(default=0)
    likes = db.ListField(db.ReferenceField(User, dbref=True))
    like_count = db.IntField(default=0)
    meta = { 'category' : 'img' }

    def is_liked(self):
        lpins = Pin.objects(likes__contains=current_user.to_dbref())
        for lpin in lpins:
            if lpin == self:
                return True
        else:
            return False
