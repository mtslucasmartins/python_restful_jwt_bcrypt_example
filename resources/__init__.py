from models.user import UserModel

from flask_restful import Resource, reqparse

from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, 
    jwt_refresh_token_required, get_jwt_identity, get_raw_jwt
)

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)


class UserLogin(Resource):

    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}
        
        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Wrong credentials'}
      
      
class UserLogoutAccess(Resource):

    def post(self):
        return {'message': 'User logout'}
      
      
class UserLogoutRefresh(Resource):

    def post(self):
        return {'message': 'User logout'}
      
      
class TokenRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}
      
class SecretResource(Resource):

    @jwt_required
    def get(self):
        return {
            'answer': 42
        }


