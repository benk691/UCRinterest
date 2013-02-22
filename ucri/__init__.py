import os
from flask import Flask, request, render_template, redirect, url_for, flash, Response, Blueprint, send_from_directory
from flask.ext.login import LoginManager, current_user, logout_user
from flask.ext.mongoengine import MongoEngine
from datetime import datetime
from werkzeug import secure_filename
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from forms import UploadForm

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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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
    upform = UploadForm()
    pins = Pin.objects.all()
    #pins = User.objects.all()
    #flash('pins = %s' % str(Pin.objects.count()))
    #flash('pins = %s' % str(User.objects.count()))
    return render_template("index.html", pins=pins, upform=upform)

@app.route('/logout')
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("index"))

# About page
@app.route('/about')
def about():
    upform = UploadForm()
    return render_template('about.html', upform=upform)

@app.route('/pin/<id>')
def bigpin(id):
	pin = Pin.objects.get(id=id)
	#user = { 'name': 'Tester' }
	return render_template('bigpin.html',
		pin = pin,
		user = current_user)

@app.route('/upload', methods=['POST'])
def upload():
    form = UploadForm()
    if form.validate():
        filename = secure_filename(form.photo.data.filename)
        form.photo.file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        pin = Pin(title=form.title.data,
                  img=filename,
                  dscrp=form.dscrp.data,
                  orig=True,
                  date=datetime.now())
        pin.save()
        flash("Image has been uploaded.")
        return redirect("/index#add_form")
    flash("Image upload error.")
    return redirect("/index#add_form")
        
@app.route('/uploads/<file>')
def uploaded_file(file):
    return send_from_directory(app.config['UPLOAD_FOLDER'], file)