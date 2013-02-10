from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "test"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"

#print dir(MongoEngine().StringField())
#print dir(MongoEngine().StringField().__init__())

db = MongoEngine(app)

if __name__ == '__main__':
    app.run()
