from database import db

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from libs.strings import gettext

from models.user import UserModel

import resources
from resources import signup as signup_resource
from resources import user as user_resource
from resources import auth as auth_resource


## 
## Flask app initilized with configurations...
application = Flask(__name__)
application.config.from_object('default_settings')

api = Api(application)

jwt = JWTManager(application)

db.init_app(application)

CORS(application)

@application.before_first_request
def create_tables():
    print('Creating Tables...')
    db.create_all()

# @jwt.user_claims_loader
# def add_claims_to_jwt(identity):
#     user = UserModel.find_by_username(identity)
#     return {'is_admin': user.is_admin}

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': gettext("security_token_expired"),
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(err):
    return jsonify({
        'description': gettext("secutity_invalid_signature"),
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(err):
    return jsonify({
        'description': gettext("security_request_without_token"),
        'error': 'token_required'
    }), 401


@jwt.needs_fresh_token_loader
def needs_fresh_token_callback():
    return jsonify({
        'description': gettext("security_token_not_fresh"),
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': gettext("security_token_revoked"),
        'error': 'token_revoked'
    }), 401


import views



# Request Token
api.add_resource(signup_resource.SignUp, '/signup')

# Users
api.add_resource(user_resource.Users, '/users')
api.add_resource(user_resource.User, '/users/<string:id>')

# Clinics
# api.add_resource(user_resource.Users, '/clinics')
# api.add_resource(user_resource.User, '/clinics/<string:id>')

# Consultations
# api.add_resource(user_resource.Users, '/clinics')
# api.add_resource(user_resource.User, '/clinics/<string:id>')

# Operator - HealthPlanOperators 
# api.add_resource(user_resource.Users, '/clinics')
# api.add_resource(user_resource.User, '/clinics/<string:id>')

# Request Token
api.add_resource(auth_resource.AuthAccessToken, '/auth/token')
api.add_resource(auth_resource.AuthRefreshToken, '/auth/refresh')

api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')

api.add_resource(resources.SecretResource, '/secret')


if __name__ == "__main__":
    application.run(debug=True, host="0.0.0.0", port=5000)
