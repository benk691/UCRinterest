import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SECRET_KEY = 'SECRET_STUFF'

HOST_URL = 'http://localhost:5000'

MONGODB_SETTINGS = { 'DB' : 'test' }
