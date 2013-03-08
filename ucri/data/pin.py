import os, re
from flask import Flask, request, render_template, redirect, url_for, flash, Response, Blueprint, send_from_directory, current_app
from flask.ext.login import current_user, login_required, confirm_login
from werkzeug import secure_filename
from mongoengine.queryset import Q
from datetime import datetime
from ucri import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from ucri.models.user import User
from ucri.models.pin import Pin
from ucri.models.comment import Comment
#from ucri.models.board import Board
from ucri.data.forms import UploadForm

mod = Blueprint('pin', __name__)

def allowed_file(filename):
    if filename != None and (type(filename) == type('') or type(filename) == type(unicode())) and '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
        return True
    flash("Failed to upload image %s. Please use an image with one of the following extensions: %s" % (str(filename), ''.join([ '%s, ' % ext for ext in ALLOWED_EXTENSIONS ]).strip(', ')))
    return False

def addInvalidBrowser(usr, invalid_usr):
    '''
    Updates the individual pin permissions of the browsers
    usr - the usr that is the pinner
    invalid_usr - the user who can't browse that users pins
    '''
    pins = Pin.objects.get(pinner=usr.to_dbref())
    for pin in pins:
        pin.invalid_browsers.append(invalid_user.to_dbref())
        pin.save()

def rmInvalidBrowser(usr, valid_usr):
    '''
    Updates the individual pin permissions of the browsers
    usr - the usr that is the pinner
    valid_usr - the user who can browse that users pins
    '''
    pins = Pin.objects.get(pinner=usr.to_dbref())
    for pin in pins:
        pin.update(pull__invalid_browsers=valid_user.to_dbref())
        pin.save()

def addInvalidCommenter(usr, invalid_usr):
    '''
    Updates the individual pin permissions of the browsers
    usr - the usr that is the pinner
    invalid_usr - the user who can't browse that users pins
    '''
    pins = Pin.objects.get(pinner=usr.to_dbref())
    for pin in pins:
        pin.invalid_commenters.append(invalid_user.to_dbref())
        pin.save()

def rmInvalidCommenter(usr, valid_usr):
    '''
    Updates the individual pin permissions of the browsers
    usr - the usr that is the pinner
    valid_usr - the user who can browse that users pins
    '''
    pins = Pin.objects.get(pinner=usr.to_dbref())
    for pin in pins:
        pin.update(pull__invalid_commenters=valid_user.to_dbref())
        pin.save()

def createPin(title, img, dscrp):
    '''Creates pin
    - title : the pin title
    - img : the image path
    - dscrp : the image description 
    '''
    if allowed_file(img):
        orig = True
        try:
            pinQuery = Pin.objects.get(img_path=img_path)
            if pinQuery is not None:
                orig = False
        except Pin.DoesNotExist:
            pass
        
        pin = Pin(title=title, img=img, pinner=current_user.to_dbref(), dscrp=dscrp, orig=orig, date=datetime.now(), repins=0, like_count=0)
        pin.save()
        if pin.repins == None:
            fix_repins()

@mod.route("/make")
def make():
    createPin("Settings 1", "img1.jpg", "Description 1")
    createPin("Settings 2", "img2.jpg", "Description 2")
    createPin("Settings 3", "img3.jpg", "Description 3")
    createPin("Settings 4", "img4.jpg", "Description 4")
    flash("Pins Created!")
    return redirect(url_for('index'))

@mod.route("/clear")
def clear():
    pins = Pin.objects.all()
    for pin in pins:
        pin.delete()
    flash("Pins deleted!")
    return redirect(url_for('index'))

@mod.route('/fix_repins')
def fix_repins():
    pins = Pin.objects.all()
    for pin in pins:
        if pin.repins == None:
            pin.repins = 0
            pin.save()
    flash("fixed repin counts")
    return(redirect("/index"))

@mod.route('/fix_likes')
def fix_likes():
    pins = Pin.objects.all()
    for pin in pins:
        if pin.like_count == None:
            pin.like_count = 0
            pin.save()
    flash("fixed like counts")
    return(redirect("/index"))

@mod.route('/pin/<id>')
def bigpin(id):
    pin = Pin.objects.get(id=id)
    #following = pin.pinner.following()
    return render_template('bigpin.html',
        pin = pin,
        #show_follow = !following,
        user = current_user)

@mod.route('/upload', methods=['POST'])
def upload():
    form = UploadForm()
    if form.validate():
        if form.title.data == "":
            flash("Must include title")
            return redirect(request.referrer + "#add_form")
        filename = secure_filename(form.photo.data.filename)
        pos = filename.rfind('.')
        if pos < 0 or (pos >= 0 and (not filename[pos + 1 : ] in ALLOWED_EXTENSIONS)):
            flash("Error: Invalid extension, pleases use jpg or png")
            return redirect(request.referrer + '#add_form')
        form.photo.file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
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

@mod.route('/repin', methods=['POST'])
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

@mod.route('/uploads/<file>')
def uploaded_file(file):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], file)

@mod.route('/search', methods = ['POST'])
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

@mod.route('/pin/<id>/edit', methods=['POST', 'GET'])
def editpin(id):
    pin = Pin.objects.get(id=id)
    if pin.pinner.id != current_user.id:
        return redirect(url_for('index'))
    if request.method == 'POST':
        pin.dscrp = request.form.get('dscrp')
        pin.save()
    return render_template("editpin.html", pin=pin, upform=UploadForm())

@mod.route('/delete', methods=['POST'])
def deletepin():
    pin = Pin.objects.get(id=request.form.get('id'))
    pin.delete()
    return redirect(url_for('index'))

@mod.route('/add_comment', methods=['POST'])
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
    
@mod.route('/like', methods=['POST'])
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

@mod.route('/favorite', methods=['POST'])
def favorite():
    id = request.form.get('id')
    pin = Pin.objects.get(id=id)
    pin.favs.append(current_user.to_dbref())
    pin.save()
    return redirect("/viewprofile/favorites")
