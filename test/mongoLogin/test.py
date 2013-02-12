from pymongo import MongoClient
from bson import Binary, Code
from bson.json_util import dumps, loads

# Create a client connection to MongoDB
connection = MongoClient('localhost', 27017)

# Grab dbs
pic_db = connection.pic
test_db = connection.test

# Grab test collection from pic db
pic = pic_db.pic
test = test_db.test

# Utility functions
def objID(collection):
    objId = collection.find({}).next()["_id"]
