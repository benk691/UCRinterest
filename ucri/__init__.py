import os
from flask import Flask, request, render_template, redirect, url_for, flash, Response, Blueprint, send_from_directory
from flask.ext.login import LoginManager, current_user, logout_user
from flask.ext.mongoengine import MongoEngine
from datetime import datetime
from werkzeug import secure_filename
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
import re
from mongoengine.queryset import Q

# Create and configure app
app = Flask(__name__)
app.config.from_object('ucri.UCRinterest.config')

# Create database
db = MongoEngine(app)

from ucri.UCRinterest.ucri.models.user import User, Anonymous
from ucri.UCRinterest.ucri.data.forms import UploadForm

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
from ucri.UCRinterest.ucri.data.help import mod as helpModule
app.register_blueprint(helpModule)

from ucri.UCRinterest.ucri.users.login import mod as loginModule
app.register_blueprint(loginModule)

from ucri.UCRinterest.ucri.users.profile import mod as profileModule
app.register_blueprint(profileModule)

from ucri.users.team import mod as teamModule
app.register_blueprint(teamModule)

from ucri.users.viewprofile import mod as viewprofileModule
app.register_blueprint(viewprofileModule)

#from ucri.data.pin import mod as pinModule
#app.register_blueprint(pinModule)

from ucri.models.pin import Pin
from ucri.models.comment import Comment

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/make")
def make():
    pin = Pin(title="Settings 1", img="img1.jpg", dscrp="Description 1", orig=True, date=datetime.now(), pinner=current_user.to_dbref())
    pin.save()
    pin = Pin(title="Settings 2", img="img2.jpg", dscrp="Description 2", orig=True, date=datetime.now(), pinner=current_user.to_dbref())
    pin.save()
    pin = Pin(title="Settings 3", img="img3.jpg", dscrp="Description 3", orig=True, date=datetime.now(), pinner=current_user.to_dbref())
    pin.save()
    pin = Pin(title="Settings 4", img="img4.jpg", dscrp="Description 4", orig=True, date=datetime.now(), pinner=current_user.to_dbref())
    pin.save()
    flash("Pins Created!")
    return redirect(url_for('index'))

@app.route("/clear")
def clear():
    pins = Pin.objects.all()
    for pin in pins:
        pin.delete()
    flash("Pins deleted!")
    return redirect(url_for('index'))

@app.route('/fix_repins')
def fix_repins():
    pins = Pin.objects.all()
    for pin in pins:
        if pin.repins == None:
            pin.repins = 0
            pin.save()
    flash("fixed repin counts")
    return(redirect("/index"))

@app.route('/fix_likes')
def fix_likes():
    pins = Pin.objects.all()
    for pin in pins:
        if pin.like_count == None:
            pin.like_count = 0
            pin.save()
    flash("fixed like counts")
    return(redirect("/index"))

# Index page
@app.route("/")
@app.route("/index")
def index():
    upform = UploadForm()
    pins = Pin.objects.order_by('-date')
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
    #following = pin.pinner.following()
	return render_template('bigpin.html',
		pin = pin,
        #show_follow = !following,
		user = current_user)

@app.route('/upload', methods=['POST'])
def upload():
    form = UploadForm()
    if form.validate():
        if form.title.data == "":
            flash("Must include title")
            return redirect(request.referrer + "#add_form")
        filename = secure_filename(form.photo.data.filename)
        pos = filename.rfind('.')
        #flash(str(filename[pos + 1: ] in ALLOWED_EXTENSIONS))
        if pos < 0 or (pos >= 0 and (not filename[pos + 1 : ] in ALLOWED_EXTENSIONS)):
            flash("Error: Invalid extension, pleases use jpg or png")
            return redirect(request.referrer + '#add_form')
        form.photo.file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        pin = Pin(title=form.title.data,
                  img=filename,
                  dscrp=form.dscrp.data,
                  orig=True,
                  date=datetime.now(),
                  pinner=current_user.to_dbref(),
                  repins=0,
                  like_count=0)
        pin.save()
        flash("Image has been uploaded.")
    else:
        flash("Image upload error.")
    return redirect(request.referrer + "#add_form" or url_for("index"))

@app.route('/repin', methods=['POST'])
def repin():
    id = request.form.get('id')
    pin = Pin.objects.get(id=id)
    newpin = Pin(title=pin.title,
                 img=pin.img,
                 dscrp=pin.dscrp,
                 orig=False,
                 date=datetime.now(),
                 pinner=current_user.to_dbref(),
                 repins=0,
                 like_count=0)
    newpin.save()
    if pin.repins == None:
        fix_repins()
        pin = Pin.objects.get(id=id)
    pin.repins = pin.repins + 1
    pin.save()
    flash("Pin repinned")
    return redirect('/viewprofile/pins')

@app.route('/uploads/<file>')
def uploaded_file(file):
    return send_from_directory(app.config['UPLOAD_FOLDER'], file)

@app.route('/search', methods = ['POST'])
def search():
    #get form input
    query = request.form.get('q')
    #tokenize
    terms = re.split('\s', query)
    #generate regular expression from tokens
    x = "|".join(map(str, terms))
    regx = re.compile(x, re.IGNORECASE)
    #query database
    pins = Pin.objects(Q(title=regx) | Q(dscrp=regx))
    return render_template("index.html", pins=pins, upform=UploadForm())

@app.route('/pin/<id>/edit', methods=['POST', 'GET'])
def editpin(id):
    pin = Pin.objects.get(id=id)
    if pin.pinner.id != current_user.id:
        return redirect(url_for('index'))
    if request.method == 'POST':
        pin.dscrp = request.form.get('dscrp')
        pin.save()
    return render_template("editpin.html", pin=pin, upform=UploadForm())

@app.route('/delete', methods=['POST'])
def deletepin():
    pin = Pin.objects.get(id=request.form.get('id'))
    pin.delete()
    return redirect(url_for('index'))

@app.route('/add_comment', methods=['POST'])
def add_comment():
    if request.form.get('val') != "":
        pin = Pin.objects.get(id=request.form.get('id'))
        comment = Comment(commenter = current_user.to_dbref(),
                          message = request.form.get('val'),
                          date = datetime.now())
        pin.cmts = pin.cmts + [comment]
        pin.save()
        flash("Comment added")
    return redirect(request.referrer)
    
@app.route('/like', methods=['POST'])
def like():
    id = request.form.get('id')
    pin = Pin.objects.get(id=id)
    if pin.is_liked() == True:
        pin.update(pull__likes=current_user.to_dbref())
        pin.like_count = pin.like_count - 1
        pin.save()
        flash("pin unliked")
        return redirect(request.referrer)
    else:
        if pin.like_count == None:
            fix_likes()
            pin = Pin.objects.get(id=id)
        pin.likes.append(current_user.to_dbref())
        pin.like_count = pin.like_count + 1
        pin.save()
        flash("pin liked")
    return redirect("/viewprofile/likes")

@app.route('/favorite', methods=['POST'])
def favorite():
    id = request.form.get('id')
    pin = Pin.objects.get(id=id)
    pin.favs.append(current_user.to_dbref())
    pin.save()
    return redirect("/viewprofile/favorites")

@app.route('/follow', methods=["POST"])
def follow():
    id = request.form.get('pinner')
    user = User.objects.get(id=id)
    current_user.follower_array.append(user)
    current_user.save()
    flash("Following " + user.uname)
    return redirect("/viewprofile/following")

@app.route('/clearfollows')
def clearfollows():
    users = User.objects
    for user in users:
        user.follower_array = None
        user.save()
    flash("Follows cleared")
    return redirect('/index')
