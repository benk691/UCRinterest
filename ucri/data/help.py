from flask import (Flask, request, render_template, redirect, url_for, flash,
                   current_app, Blueprint)
from ucri.data.forms import UploadForm

mod = Blueprint('help', __name__)

@mod.route('/help')
def help():
    upform = UploadForm()
    return render_template('help.html', upform=upform)

# About page
@mod.route('/about')
def about():
    upform = UploadForm()
    return render_template('about.html', upform=upform)

