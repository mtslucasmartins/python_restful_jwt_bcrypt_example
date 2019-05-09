
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, 
    jwt_refresh_token_required, get_jwt_identity, get_raw_jwt
)
from libs.strings import gettext
from models.user import UserModel


def parse_auth_token_args():
    parser = reqparse.RequestParser()
    parser.add_argument('username', help = 'This field cannot be blank', required=True)
    parser.add_argument('password', help = 'This field cannot be blank', required=True)
    return parser.parse_args();


class AuthAccessToken(Resource):

    def post(self):
        request_args = parse_auth_token_args()

        username = request_args.get('username')
        password = request_args.get('password')

        current_user = UserModel.find_by_email(username)
    
        if not current_user:
            return ({
                'description': gettext("security_invalid_credentials"),
                'error': 'invalid_credentials'
            }, 401)

        if UserModel.verify_hash(password, current_user.password):
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            return {
                'token_type': 'Bearer',
                'access_token': access_token,
                'refresh_token': refresh_token
            }    

        return ({
            'description': gettext("security_request_without_token"),
            'error': 'invalid_credentials'
        }, 401)
      

class AuthRefreshToken(Resource):
    
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}