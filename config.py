import os
_basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True

DEBUG = True

SECRET_KEY = 'SECRET_STUFF'

UPLOAD_FOLDER = '/photos'

HOST_URL = 'http://localhost:5000'

MONGODB_SETTINGS = { 'DB' : 'test' }

