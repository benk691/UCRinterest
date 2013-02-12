from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "test"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"
app.config["DEBUG"] = True

db = MongoEngine(app)

# Login manager
#login_manager = LoginManager(app)
'''
# Configure app for login 
login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"
login_manager.login_message = u"Log In"
login_manager.refresh_view = "reauth"
login_manager.setup_app(app)
'''

if __name__ == "__main__":
    app.run()
