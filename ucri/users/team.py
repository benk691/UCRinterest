from flask import (Flask, request, render_template, redirect, url_for, flash,
                   current_app, Blueprint)
from flask.ext.login import (current_user, login_required, confirm_login,
                             fresh_login_required)

mod = Blueprint('team', __name__)

@mod.route('/team')
def team():
    return render_template('team.html')
