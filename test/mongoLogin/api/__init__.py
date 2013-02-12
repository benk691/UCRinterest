from flask import Flask
from flask.ext.mongoengine import MongoEngine
#from flask.ext.mongokit import MongoKit

app = Flask(__name__, static_folder='../static', template_folder='../templates')
app.config["MONGODB_SETTINGS"] = {'DB': "test"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"
app.config["DEBUG"] = True

db = MongoEngine(app)
