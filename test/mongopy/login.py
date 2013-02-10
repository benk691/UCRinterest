from flask import Flask
from flask.ext.login import *

# Flask application
app = Flask(__name__)

# Login manager
login_manager = LoginManager()

# Configure app for login 
login_manager.setup_app(app)

@login_manager.user_loader
def load_user(user_id):
    '''user_loader callback. This callback is used to
    reload the user object from the user ID stored in the 
    session
    @param user_id A unicode ID of a user
    @return corresponding user object if ID exists, otherwise return None
    '''
    return None
