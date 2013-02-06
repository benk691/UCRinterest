from flask import Flask
from flask.ext.mongoengine import MongoEngine
import mongoengine

app = Flask(__name__)
#app.config["MONGODB_SETTINGS"] = {'DB' : "my_tumble_log"}
#app.config["MONGODB_SETTINGS"] = {'DB' : "test"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"

print dir(mongoengine)
mongoengine.connect('ucrinterest', host='ec2-50-18-9-255.us-west-1.compute.amazonaws.com', port=27017)
#mongoengine.connect('ucrinterest', host='mongodb://ec2-50-18-9-255.us-west-1.compute.amazonaws.com/test')
db = MongoEngine(app)

def register_blueprints(app):
    # Prevents circular imports
    from tumblelog.views import posts
    app.register_blueprint(posts)

register_blueprints(app)

if __name__ == '__main__':
	app.run()
