from flask import Flask, request, render_template, redirect, url_for, flash, current_app, Blueprint
from flask.ext.login import (current_user, login_required, confirm_login, fresh_login_required)
from forms import RegisterForm
from datetime import datetime
from ucri.UCRinterest.ucri.models.user import User

# Profile blueprint
mod = Blueprint('profile', __name__)

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
                usr = User(uname=form.uname.data, fname=form.fname.data, lname=form.lname.data, email=form.email.data, gender=form.gender.data, pwd=form.pwd.data, dscrp=form.dscrp.data, bday=form.bday.data, creation_date=datetime.now())
                usr.save()
                flash('Thanks for registering!')
                return redirect(url_for('login.login'))
        except User.DoesNotExist:
            usr = User(uname=form.uname.data, fname=form.fname.data, lname=form.lname.data, email=form.email.data, gender=form.gender.data, pwd=form.pwd.data, dscrp=form.dscrp.data, bday=form.bday.data, creation_date=datetime.now())
            usr.save()
            flash('Thanks for registering!')
            return redirect(url_for('login.login'))
    return render_template('register.html', form=form)
