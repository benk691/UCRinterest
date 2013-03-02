from ucri import db
from settings import *
from user import User

class Comment(db.EmbeddedDocument):
	commenter = db.ReferenceField(User, dbref=True, required=True)
	message = db.StringField(min_length=DSCRPT_MIN_LENGTH+1, max_length=DSCRPT_MAX_LENGTH, required=True)
	date = db.DateTimeField(required=True)
