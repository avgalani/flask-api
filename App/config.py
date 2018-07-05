__author__ = 'Alex Galani'

# Flask
DEBUG = True

# Database
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Flask-Security
SECRET_KEY = 'my_secret_key'
SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'
WTF_CSRF_ENABLED = False
SECURITY_TOKEN_MAX_AGE = 86400
SECURITY_UNAUTHORIZED_VIEW = '/'