from flask import (Flask, request, render_template, redirect, url_for, flash,
                   current_app, Blueprint)
from flask.ext.login import (current_user, login_required, confirm_login,
                             fresh_login_required)
from datetime import datetime
from ucri.models.user import User
#from ucri.models.pin import Pin
from ucri.models.album import Album

mod = Blueprint('viewpin', __name__)

@mod.route('/pin/<id>')
@login_required
def viewpin():
    return render_template('pin.html')
