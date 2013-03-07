import os
from bcrypt import hashpw, gensalt
from PIL import Image
from flask import Flask, request, render_template, redirect, url_for, flash, current_app, Blueprint
from flask.ext.login import current_user, login_required, confirm_login, fresh_login_required
from flask.ext.uploads import (UploadSet, configure_uploads, IMAGES,
                              UploadNotAllowed)
from werkzeug import secure_filename
from datetime import datetime
from forms import RegisterForm, SettingsForm, PasswordForm, InterestForm
from ucri import DEFAULT_PROFILE_PIC, DEFAULT_PROFILE_PIC_PATH, DEFAULT_PROFILE_PIC_LOC
from ucri.models.user import User
from ucri.data.forms import UploadForm
from ucri.data.pin import ALLOWED_EXTENSIONS, allowed_file

# Profile blueprint
mod = Blueprint('profile', __name__)

def createNewUser(form):
    hashedpwd = hashpw(form.pwd.data, gensalt(log_rounds=13))
    usr = User(uname=form.uname.data,
               fname=form.fname.data,
               lname=form.lname.data,
               img_path = DEFAULT_PROFILE_PIC,
               email=form.email.data,
               gender=form.gender.data,
               pwd=hashedpwd,
               dscrp=form.dscrp.data,
               bday=form.bday.data,
               creation_date=datetime.now())
    usr.img = Image.open(DEFAULT_PROFILE_PIC_PATH)
    def_img = open(DEFAULT_PROFILE_PIC_LOC, 'r')
    usr.img_file = def_img
    usr.img_file.content_type = 'image/jpeg'
    usr.save()
    flash('Thanks for registering!')
    return redirect(url_for('login.login'))

@mod.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            usrQuery = User.objects.get(uname=form.data['uname'])
            if usrQuery is not None:
                flash('Username already exists!')
                redirect(url_for('profile.register'))
            else:
                return createNewUser(form)
        except User.DoesNotExist:
            return createNewUser(form)
    return render_template('register.html', form=form)

########## Settings ##########
def changeProfilePic(form):
    if form.validate():
        flash(str(form.img.data.filename))
    else:
        flash("No validate")
    return render_template("settings.html", form=form, upform=UploadForm())
    """
    filename = form.img.data
    if form.validate() and filename != DEFAULT_PROFILE_PIC and allowed_file(filename):
        # Store file
        filename = secure_filename(filename)
        form.img.file = open(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        form.img.file.save()
        # Save to DB
        current_user.img = filename
        current_user.save()
        flash("Successfully changed profile picture to %s" % filename)
        return render_template("settings.html", form=form, upform=UploadForm())
    flash("Failed to upload profile picture. Please use an image with one of the following extensions: %s" % (''.join([ '%s, ' % ext for ext in ALLOWED_EXTENSIONS ]).strip(', ')))
    return render_template("settings.html", form=form, upform=UploadForm())
    """

@mod.route('/settings', methods=['GET', 'POST'])
@login_required
def profileSettings():
    form = SettingsForm(request.form, obj=current_user)
    if request.method == 'POST':
        # Handle changing password
        if form.data['change_pwd']:
            return redirect(url_for('profile.setPassword'))
        # Handle changing profile pic
        if len(form.data['img']) > 0 and form.data['img'] != DEFAULT_PROFILE_PIC:
            return changeProfilePic(form)
        return redirect("/viewprofile/pins")
    return render_template("settings.html", form=form, upform=UploadForm())

@mod.route('/settings/pwd', methods=['GET', 'POST'])
@login_required
def setPassword():
    form = PasswordForm(request.form)
    if request.method == "POST" and form.validate():
        hashedpwd = hashpw(form.pwd.data, gensalt(log_rounds=13))
        current_user.pwd = hashedpwd
        current_user.save()
        flash("Password was changed successfully")
        return redirect('/settings')
    return render_template("newpassword.html", form=form, upform=UploadForm())

##############################

@mod.route('/interests', methods=['GET', 'POST'])
def addInterests():
    form = InterestForm(request.form)
    if request.method == 'POST' and form.validate():     
        pass

@mod.route('/follow', methods=["POST"])
def follow():
    id = request.form.get('pinner')
    user = User.objects.get(id=id)
    current_user.follower_array.append(user)
    current_user.save()
    flash("Following " + user.uname)
    return redirect("/viewprofile/following")

@mod.route('/clearfollows')
def clearfollows():
    users = User.objects
    for user in users:
        user.follower_array = None
        user.save()
    flash("Follows cleared")
    return redirect('/index')
