##################################################
# Init
##################################################
from flask import Flask, request, render_template, redirect, url_for, flash, Response, Blueprint, send_from_directory
from flask.ext.login import LoginManager, current_user, logout_user, login_required
from flask.ext.mongoengine import MongoEngine
from datetime import datetime
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, DEFAULT_PROFILE_PIC, DEFAULT_PROFILE_PIC_PATH, DEFAULT_PROFILE_PIC_LOC

# Create and configure app
app = Flask(__name__)
app.config.from_object('config')

# Create database
db = MongoEngine(app)

from ucri.models.user import User, Anonymous
from ucri.models.pin import Pin
from ucri.data.forms import UploadForm
from ucri.data.pin import getValidBrowserPins
from ucri.users.profile import handleUserDeletion

# Login manager
login_manager = LoginManager()

# Configure app for login 
login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"
login_manager.login_message = u"Log In"
login_manager.refresh_view = "reauth"
login_manager.setup_app(app)

# Load user
@login_manager.user_loader
def load_user(user_id):
    '''user_loader callback. This callback is used to
    reload the user object from the user ID stored in the 
    session
    @param user_id A unicode ID of a user
    @return corresponding user object if ID exists, otherwise return None
    '''
    return User.objects.get(uname=user_id)

# Error handler
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error), 404

# Register blueprints
from ucri.data.help import mod as helpModule
app.register_blueprint(helpModule)

from ucri.users.login import mod as loginModule
app.register_blueprint(loginModule)

from ucri.users.profile import mod as profileModule
app.register_blueprint(profileModule)

from ucri.users.team import mod as teamModule
app.register_blueprint(teamModule)

from ucri.users.viewprofile import mod as viewprofileModule
app.register_blueprint(viewprofileModule)

from ucri.data.pin import mod as pinModule
app.register_blueprint(pinModule)

# Index page
@app.route("/")
@app.route("/index")
def index():
    upform = UploadForm()
    pins = Pin.objects.order_by('-date')
    valid_pins = getValidBrowserPins(pins, current_user)
    return render_template("index.html", pins=valid_pins, upform=upform)

@app.route("/clear")
def clear():
    # logout the users
    if current_user == None or not current_user.is_active():
        # Delete users
        usrs = User.objects.all()
        for usr in usrs:
            handleUserDeletion(usr)
        flash("Everything deleted!")
    else:
        flash("No users can be logged in")
    return redirect(url_for('index'))
