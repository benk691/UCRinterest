from flask import Flask, request, render_template, redirect, url_for, flash, Response
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)
from api import app, db
from user import User, Anonymous

# Login manager
login_manager = LoginManager()

# Configure app for login 
login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"
login_manager.login_message = u"Log In"
login_manager.refresh_view = "reauth"
login_manager.setup_app(app)

@login_manager.user_loader
def load_user(user_id):
    '''user_loader callback. This callback is used to
    reload the user object from the user ID stored in the 
    session
    @param user_id A unicode ID of a user
    @return corresponding user object if ID exists, otherwise return None
    '''
    return User.objects.get(uname=user_id)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/secret")
@fresh_login_required
def secret():
    return render_template("secret.html")

@app.route("/login", methods=["GET", "POST"])
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

@app.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        flash(u"Reauthenticated.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("reauth.html")

@app.route("/index")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run()
