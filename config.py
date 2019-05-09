import os 

# Application
SECRET_KEY = os.urandom(24)
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = os.environ.get('PORT', 5000)

# Database
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT
# JWT_MAX_VALIDITY = 3600 # 1 hour
JWT_SECRET_KEY = os.urandom(24)