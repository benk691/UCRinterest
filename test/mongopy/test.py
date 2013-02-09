from pymongo import MongoClient
from bson import Binary, Code
from bson.json_util import dumps, loads

# Create a client connection to MongoDB
connection = MongoClient('localhost', 27017)

# Grab test db
db = connection.test

# Grab test collection from test db
test = db.test

for item in test.find():
    print item

# Utility functions
def objID(collection):
    objId = collection.find({}).next()["_id"]

print objId
