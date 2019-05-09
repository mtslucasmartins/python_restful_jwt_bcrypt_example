import os 
import datetime as dt

# Application
SECRET_KEY = os.urandom(24)
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = os.environ.get('PORT', 5000)


# Database
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

# JWT
JWT_SECRET_KEY = os.urandom(24)
JWT_EXPIRATION_DELTA = dt.timedelta(seconds=3600) # a datetime.timedelta indicating how long tokens are valid for.
JWT_ACCESS_TOKEN_EXPIRES = dt.timedelta(seconds=3600)
JWT_REFRESH_TOKEN_EXPIRES = dt.timedelta(days=30)

# RESTful
BUNDLE_ERRORS = True