from flask import (Flask, request, render_template, redirect, url_for, flash,
                   current_app, Blueprint)
from flask.ext.login import (current_user, login_required, confirm_login,
                             fresh_login_required)
from datetime import datetime
from ucri.models.user import User
from ucri.models.pin import Pin
#from ucri.models.album import Album

mod = Blueprint('pin', __name__)

"""
@mod.route('/pin/<id>')
@login_required
def viewpin():
    return render_template('pin.html')
"""

@mod.route('/pin/<id>', methods=['POST'])
#@login_required
def remove(id):
    pin = Pin.objects.get(id=id)
    if request.method == 'POST':
        pin.delete()
        redirect("bigpin.html", pin=pin, user=current_user)
        #return redirect(url_for("index"))
    return redirect("bigpin.html", pin=pin, user=current_user)
