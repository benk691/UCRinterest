from flask import Flask, request, render_template, redirect, url_for, flash
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)
from api import db

##########
# TODO: 
#   - Figure out how to incorporate mongoDB into the login
#   - Look at the flask-login example page and look at the USERS array
##########
class User(UserMixin, db.Document):
    '''User database model. Fields:
    - uname : user name, this needs to be unique
    - fname : first name
    - lname : last name
    - email : email address
    - pwd   : password
    - img_array : array of img ids
    '''
    uname = db.StringField(min_length=3, max_length=25, unique=True, required=True)
    pwd = db.StringField(min_length=3, max_length=50, required=True)

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.uname)

class Anonymous(AnonymousUser):
    name = u"Anonymous"


