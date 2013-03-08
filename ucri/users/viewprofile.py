from flask import (Flask, request, render_template, redirect, url_for, flash,
                   current_app, Blueprint)
from flask.ext.login import (current_user, login_required, confirm_login,
                             fresh_login_required)
from datetime import datetime
#from ucri.models.board import Board
from ucri.models.user import User
from ucri.models.pin import Pin
from ucri.data.forms import UploadForm

mod = Blueprint('viewprofile', __name__)

@mod.route('/viewprofile/<uname>/')
@login_required
def profile(uname):
    user = User.objects.get(uname=uname)
    return render_template('viewprofile.html', upform=UploadForm(), user=user)

@mod.route('/viewprofile/<uname>/pins')
@login_required
def profilepins(uname):
    user = User.objects.get(uname=uname)
    pins = Pin.objects(pinner=user.to_dbref()).order_by('-date')
    return render_template('profilepins.html', pins=pins, upform=UploadForm(), user=user)

@mod.route('/viewprofile/<uname>/likes')
@login_required
def likedpins(uname):
    user = User.objects.get(uname=uname)
    pins = Pin.objects(likes__contains=user.to_dbref())
    return render_template('profilepins.html', pins=pins, upform=UploadForm(), user=user)

@mod.route('/viewprofile/<uname>/favorites')
@login_required
def favorites(uname):
    user = User.objects.get(uname=uname)
    pins = Pin.objects(favs__contains=user.to_dbref())
    return render_template('profilepins.html', pins=pins, upform=UploadForm(), user=user)

@mod.route('/viewprofile/<uname>/following')
@login_required
def following(uname):
    user=User.objects.get(uname=uname)
    users = user.follower_array
    return render_template('profilefollows.html', users=users, upform=UploadForm(), user=user)

@mod.route('/viewprofile/<uname>/followers')
@login_required
def followers(uname):
    user = User.objects.get(uname=uname)
    users = User.objects.filter(follower_array__contains=user.to_dbref())
    return render_template('profilefollows.html', users=users, upform=UploadForm(), user=user)
