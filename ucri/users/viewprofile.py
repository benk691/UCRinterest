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

@mod.route('/viewprofile/<id>')
@login_required
def viewprofile(id):
    user = User.objects.get(id=id)
    return render_template('viewprofile.html', user=user, upform=UploadForm())

@mod.route('/viewprofile/<id>/pins')
@login_required
def profilepins(id):
    user = User.objects.get(id=id)
    pins = Pin.objects(pinner=user.to_dbref()).order_by('-date')
    return render_template('profilepins.html', user=user, pins=pins, upform=UploadForm())

@mod.route('/viewprofile/<id>/likes')
@login_required
def likedpins(id):
    user = User.objects.get(id=id)
    pins = Pin.objects(likes__contains=user.to_dbref())
    return render_template('profilepins.html',user=user, pins=pins, upform=UploadForm())

@mod.route('/viewprofile/<id>/favorites')
@login_required
def favorites(id):
    user = User.objects.get(id=id)
    pins = Pin.objects(favs__contains=user.to_dbref())
    return render_template('profilepins.html', user=user, pins=pins, upform=UploadForm())

@mod.route('/viewprofile/<id>/following')
@login_required
def following(id):
    user = User.objects.get(id=id)
    users = user.follower_array
    return render_template('profilefollows.html', user=user, users=users, upform=UploadForm())

@mod.route('/viewprofile/<id>/followers')
@login_required
def followers(id):
    user = User.objects.get(id=id)
    users = User.objects.filter(follower_array__contains=user.to_dbref())
    return render_template('profilefollows.html', user=user, users=users, upform=UploadForm())
