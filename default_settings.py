import os 
import datetime as dt

# Application
SECRET_KEY = os.urandom(24)

# Database
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT
JWT_SECRET_KEY = os.urandom(24)
JWT_EXPIRATION_DELTA = dt.timedelta(seconds=3600) # a datetime.timedelta indicating how long tokens are valid for.