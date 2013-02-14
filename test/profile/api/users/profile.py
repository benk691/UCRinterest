from flask import Flask, request, render_template, redirect, url_for, flash, current_app, Blueprint
from flask.ext.login import (current_user, login_required, confirm_login, fresh_login_required)
from forms import RegisterForm
from datetime import datetime
#from api import db
from api.models.user import User

# Profile blueprint
mod = Blueprint('profile', __name__)

@mod.route('/register', methods=['GET', 'POST'])
def register():
    flash('Register!')
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        flash('You are registering with POST!')
        usr = User(uname=form.uname.data, fname=form.fname.data, lname=form.lname.data, email=form.email.data, gender=form.gender.data, pwd=form.pwd.data, dscrp=form.dscrp.data, bday=form.bday.data, creation_date=datetime.now())
        print 'User =', str(usr)
        usr.save()
        flash('Thanks for registering')
        return redirect(url_for('login'))
    elif request.method == 'GET':
        flash('You are registering with GET!')
    elif not form.validate():
        flash('Form not validated')
    return render_template('register.html', form=form)
