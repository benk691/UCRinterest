from flask import Flask, request, render_template, redirect, url_for, flash, current_app, Blueprint
from flask.ext.login import (current_user, login_required, confirm_login, fresh_login_required)
from forms import RegisterForm
from datetime import datetime
from api.models.user import User

# Profile blueprint
mod = Blueprint('profile', __name__)

@mod.route('/register', methods=['GET', 'POST'])
def register():
    flash('Register!')
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            usrQuery = User.objects.get(uname=form.data['uname'])
            if usrQuery is not None:
                flash('Username already exists!')
                redirect(url_for('profile.register'))
            else:
                usr = User(uname=form.uname.data, fname=form.fname.data, lname=form.lname.data, email=form.email.data, gender=form.gender.data, pwd=form.pwd.data, dscrp=form.dscrp.data, bday=form.bday.data, creation_date=datetime.now())
                usr.save()
                flash('Thanks for registering!')
                return redirect(url_for('login.login'))
        except User.DoesNotExist:
            usr = User(uname=form.uname.data, fname=form.fname.data, lname=form.lname.data, email=form.email.data, gender=form.gender.data, pwd=form.pwd.data, dscrp=form.dscrp.data, bday=form.bday.data, creation_date=datetime.now())
            usr.save()
            flash('Thanks for registering!')
            return redirect(url_for('login.login'))
    elif request.method == 'GET' and form.validate():
        flash('You are registering with GET!')
    elif request.method in ['GET', 'POST'] and not form.validate():
        flash('Form not validated!')
        flash('request.method = %s' % request.method)
    else:
        flash('request.method = %s' % request.method)
        flash('A Dark Wizard has casted an evil curse on your site!')
    return render_template('register.html', form=form)
