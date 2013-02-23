from flask import (Flask, request, render_template, redirect, url_for, flash,
                   current_app, Blueprint)
from flask.ext.login import (current_user, login_required, confirm_login,
                             fresh_login_required)
from datetime import datetime
from ucri.models.user import User
#from ucri.models.album import Album
from ucri.models.pin import Pin

from ucri import UploadForm

mod = Blueprint('viewprofile', __name__)

@mod.route('/viewprofile')
@login_required
def viewprofile():
    pins = Pin.objects(pinner=current_user.to_dbref()).order_by('-date')
    return render_template('viewprofile.html', pins=pins, upform=UploadForm())
