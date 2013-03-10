##################################################
# The library functions for the pin database model
# This defines the required document as well as easy-to-use functions to get user information
##################################################
from flask.ext.login import current_user
from ucri.UCRinterest.ucri import db
from settings import *
from user import User
from comment import Comment

class Pin(db.Document):
    '''Pin collection model. Fields:
    - title : title of the pin
    - dscrp : description
    - date : date format
    - cat : category
    - img : image
    - cmts : a list of comments
    - repins : count of repins
    - likes : list of users who have liked
    - like_count : count of likes
    - favs : list of users who have added pin to favorites
    '''
    title = db.StringField(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH, required=True)
    img = db.StringField(min_length=PATH_MIN_LENGTH, required=True)
    pinner = db.ReferenceField(User, reverse_delete_rule=db.CASCADE, dbref=True, required=True)
    orig = db.BooleanField(required=True)
    dscrp = db.StringField(min_length=DSCRPT_MIN_LENGTH, max_length=DSCRPT_MAX_LENGTH)
    date = db.DateTimeField(required=True)
    cmts = db.ListField(db.EmbeddedDocumentField(Comment))
    repins = db.IntField(default=0)
    likes = db.ListField(db.ReferenceField(User, reverse_delete_rule=db.PULL, dbref=True))
    like_count = db.IntField(default=0)
    favs = db.ListField(db.ReferenceField(User, reverse_delete_rule=db.PULL, dbref=True))
    invalid_browsers = db.ListField(db.ReferenceField(User, reverse_delete_rule=db.PULL, dbref=True))
    invalid_commenters = db.ListField(db.ReferenceField(User, reverse_delete_rule=db.PULL, dbref=True))
    meta = { 'category' : 'img' }

    def is_liked(self):
        lpins = Pin.objects(likes__contains=current_user.to_dbref())
        for lpin in lpins:
            if lpin == self:
                return True
            else:
                return False

    def validCommenter(self):
        '''
        Get the valid commenters, to comment a user has to be logged in
        '''
        # Check that the pins param is valid
        for iusr in self.invalid_commenters:
            if iusr.uname == current_user.uname:
                return False
        return True
