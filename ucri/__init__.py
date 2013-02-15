from flask import Flask, request, render_template, redirect, url_for, flash, Response, Blueprint
from flask.ext.login import LoginManager, current_user, logout_user
from flask.ext.mongoengine import MongoEngine

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

from ucri.users.viewprofile import mod as viewprofileModule
app.register_blueprint(viewprofileModule)

from ucri.users.pin import mod as pinModule
app.register_blueprint(pinModule)

# Index page
@app.route("/")
@app.route("/index")
def index():
    pins = [
			{
				'id': '1',
				'title': 'Sample 1',
				'pinner': { 'name': 'Perp1' },
				'image': 'img1.jpg',
				'desc': 'Description 1'
			},
			{
				'id': '2',
				'title': 'Sample 2',
				'pinner': { 'name': 'Perp1' },
				'image': 'img2.jpg',
				'desc': 'Description 2'
			},
			{
				'id': '3',
				'title': 'Sample 3',
				'pinner': { 'name': 'Perp2' },
				'image': 'img3.jpg',
				'desc': 'Description 3'
			},
			{
				'id': '4',
				'title': 'Sample 4',
				'pinner': { 'name': 'Perp1' },
				'image': 'img4.jpg',
				'desc': 'Description 4'
			},
			{
				'id': '5',
				'title': 'Sample 5',
				'pinner': { 'name': 'Perp2' },
				'image': 'img5.jpg',
				'desc': 'Description 5'
			}
		]
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
	pin = {
				'id': '1',
				'title': 'Sample 1',
				'pinner': { 'name': 'Perp1' },
				'image': 'img1.jpg',
				'desc': 'Description 1'
			}
	user = { 'name': 'Tester' }
	return render_template('bigpin.html',
		pin = pin,
		user = current_user)
