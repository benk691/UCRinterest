from flask import Flask, request, render_template, redirect, url_for, flash, Response, Blueprint
from flask.ext.login import LoginManager
from flask.ext.mongoengine import MongoEngine

# Create and configure app
app = Flask(__name__)
app.config.from_object('ucri.UCRinterest.config')

# Create database
db = MongoEngine(app)

from ucri.UCRinterest.ucri.models.user import User, Anonymous

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
from ucri.UCRinterest.ucri.users.login import mod as loginModule
app.register_blueprint(loginModule)

from ucri.UCRinterest.ucri.users.profile import mod as profileModule
app.register_blueprint(profileModule)

# Index page
@app.route("/")
def index():
    return render_template("index.html")

