from flask import Flask, request, render_template, redirect, url_for, flash, Response, Blueprint
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)
#from api import app, db
from api.models.user import User, Anonymous

# Login blueprint
mod = Blueprint('login', __name__)

@mod.route("/secret")
@fresh_login_required
def secret():
    return render_template("secret.html")

@mod.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "username" in request.form and "password" in request.form:
        # get username and password from HTML Fields
        username = request.form["username"]
        password = request.form["password"]
        # Query database
        try:
            usrQuery = User.objects.get(uname=username)
            if usrQuery is not None and usrQuery.pwd == password:
                if login_user(usrQuery, remember="no"):
                    flash("Logged in!")
                    return redirect(request.args.get("next") or url_for("index"))
                else:
                    flash("Sorry, but you could not log in.")
            else:
                flash(u"Invalid username.")
        except User.DoesNotExist:
            flash(u"Invalid username.")
    return render_template("login.html")

@mod.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        flash(u"Reauthenticated.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("reauth.html")

@mod.route("/index")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("index"))