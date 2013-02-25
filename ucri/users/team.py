from flask import (Flask, request, render_template, redirect, url_for, flash,
                   current_app, Blueprint)

mod = Blueprint('team', __name__)

@mod.route('/team')
def team():
    return render_template('team.html')
