from flask import (Flask, request, render_template, redirect, url_for, flash,
                   current_app, Blueprint)
from flask.ext.login import (current_user, login_required, confirm_login,
                             fresh_login_required)
from datetime import datetime
from ucri.UCRinterest.ucri.models.user import User
#from ucri.UCRinterest.ucri.models.board import Board

mod = Blueprint('viewpin', __name__)

@mod.route('/pin/<id>')
@login_required
def viewpin():
    return render_template('pin.html')
