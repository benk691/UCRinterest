from flask import Flask, request, render_template, redirect, url_for, flash, Response, Blueprint
from flask.ext.login import LoginManager, current_user, logout_user
from flask.ext.mongoengine import MongoEngine
from datetime import datetime

# Create and configure app
app = Flask(__name__)
app.config.from_object('config')

# Create database
db = MongoEngine(app)

from ucri.models.user import User, Anonymous

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
from ucri.users.login import mod as loginModule
app.register_blueprint(loginModule)

from ucri.users.profile import mod as profileModule
app.register_blueprint(profileModule)

from ucri.users.team import mod as teamModule
app.register_blueprint(teamModule)

from ucri.users.viewprofile import mod as viewprofileModule
app.register_blueprint(viewprofileModule)

#from ucri.users.pin import mod as pinModule
#app.register_blueprint(pinModule)

from ucri.models.pin import Pin

@app.route("/make")
def make():
    pin = Pin(title="Settings 1", img="img1.jpg", dscrp="Description 1", orig=True, date=datetime.now())
    pin.save()
    pin = Pin(title="Settings 2", img="img2.jpg", dscrp="Description 2", orig=True, date=datetime.now())
    pin.save()
    pin = Pin(title="Settings 3", img="img3.jpg", dscrp="Description 3", orig=True, date=datetime.now())
    pin.save()
    pin = Pin(title="Settings 4", img="img4.jpg", dscrp="Description 4", orig=True, date=datetime.now())
    pin.save()
    flash("Pins Created!")
    return redirect(url_for('index'))

# Index page
@app.route("/")
@app.route("/index")
def index():
    pins = Pin.objects.all()
    #pins = User.objects.all()
    flash('pins = %s' % str(Pin.objects.count()))
    #flash('pins = %s' % str(User.objects.count()))
    return render_template("index.html", pins=pins)

@app.route('/logout')
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("index"))

# About page
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/pin/<id>')
def bigpin(id):
	pin = Pin.objects.get(id=id)
	#user = { 'name': 'Tester' }
	return render_template('bigpin.html',
		pin = pin,
		user = current_user)
