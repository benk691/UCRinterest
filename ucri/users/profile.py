from bcrypt import hashpw, gensalt
from flask import Flask, request, render_template, redirect, url_for, flash, current_app, Blueprint
from flask.ext.login import current_user, login_required, confirm_login, fresh_login_required
from forms import RegisterForm, SettingsForm, InterestForm
from datetime import datetime
from ucri.models.user import User
from ucri.data.forms import UploadForm

# Profile blueprint
mod = Blueprint('profile', __name__)

def createNewUser(form):
    hashedpwd = hashpw(form.pwd.data, gensalt(log_rounds=13))
    usr = User(uname=form.uname.data,
               fname=form.fname.data,
               lname=form.lname.data,
               email=form.email.data,
               gender=form.gender.data,
               pwd=hashedpwd,
               dscrp=form.dscrp.data,
               bday=form.bday.data,
               creation_date=datetime.now())
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

@mod.route('/settings', methods=['GET', 'POST'])
def profileSettings():
    form = SettingsForm(request.form)
    return render_template("settings.html", form=form, upform=UploadForm())

@mod.route('/settings/email', methods=['GET', 'POST'])
def setEmail():
    form = SettingsForm(request.form)
    return render_template("settings.html", form=form, upform=UploadForm())

@mod.route('/settings/pwd', methods=['GET', 'POST'])
def setPassword():
    form = SettingsForm(request.form)
    return render_template("settings.html", form=form, upform=UploadForm())

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
