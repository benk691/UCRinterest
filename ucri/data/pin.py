from flask import (Flask, request, render_template, redirect, url_for, flash,
                   current_app, Blueprint)
from flask.ext.login import (current_user, login_required, confirm_login,
                             fresh_login_required)
from datetime import datetime
from ucri.models.user import User
from ucri.models.pin import Pin
#from ucri.models.album import Album

mod = Blueprint('pin', __name__)

@mod.route('/pin/<id>')
@login_required
def viewpin():
    return render_template('pin.html')

@login_required
def createPin(title, img_path, dscrp):
    orig = True
    try:
        pinQuery = Pin.objects.get(img_path=img_path)
        if pinQuery is not None:
            orig = False
    except Pin.DoesNotExist:
        pass

    pin = Pin(title=title, img_path=img_path, pinner=current_user, dscrp=dscrp, orig=orig, date=datetime.now())
