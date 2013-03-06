import os

CSRF_ENABLED = True

DEBUG = True

SECRET_KEY = 'SECRET_STUFF'

ALLOWED_EXTENSIONS = set(['apng', 'png', 'jpg', 'jpeg', 'gif'])

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'photos')

FILE_SYSTEM_STORAGE_FILE_VIEW = 'static'

#DEFAULT_PROFILE_PIC = UPLOAD_FOLEDER + '/_default_profile_pic.jpg'
DEFAULT_PROFILE_PIC = '_default_profile_pic_.jpg'

HOST_URL = 'http://localhost:5000'

MONGODB_SETTINGS = { 'DB' : 'test' }

