from flask import (Flask, request, render_template, redirect, url_for, flash,
                   current_app, Blueprint)

mod = Blueprint('help', __name__)

@mod.route('/help')
def help():
    return render_template('help.html')
