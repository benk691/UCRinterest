import os

CSRF_ENABLED = True

DEBUG = False

SECRET_KEY = 'SECRET_STUFF'

ALLOWED_EXTENSIONS = set(['bmp', 'apng', 'png', 'jpg', 'jpeg', 'gif', 'BMP', 'APNG', 'PNG', 'JPG', 'JPEG', 'GIF'])

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'photos')

FILE_SYSTEM_STORAGE_FILE_VIEW = 'static'

DEFAULT_PROFILE_PIC = '_default_profile_pic_.jpg'

DEFAULT_PROFILE_PIC_LOC = 'photos/_default_profile_pic_.jpg'

DEFAULT_PROFILE_PIC_PATH = UPLOAD_FOLDER + '/' + DEFAULT_PROFILE_PIC

HOST_URL = 'http://localhost:5000'

MONGODB_SETTINGS = { 'DB' : 'test' }

