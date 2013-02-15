import os
_basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True

DEBUG = True

SECRET_KEY = 'SECRET_STUFF'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg'])

UPLOAD_FOLDER = os.path.realpath('.') + '/photos/'

FILE_SYSTEM_STORAGE_FILE_VIEW = 'static'

HOST_URL = 'http://localhost:5000'

MONGODB_SETTINGS = { 'DB' : 'test' }

