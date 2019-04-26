from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, 
    jwt_refresh_token_required, get_jwt_identity, get_raw_jwt
)

from libs.strings import gettext
from models import UserModel


class User(Resource):

    @jwt_required
    def get(self, username: str):
        user = UserModel.find_by_username(username)
        if not user:
            return { 'message': gettext("user_not_found") }, 404
        return user.json(), 200

    @jwt_required
    def delete(self, username: str):
        user = UserModel.find_by_username(username)
        if not user:
            return {'message': gettext("user_not_found")}, 404
        user.delete()
        return {'message': gettext("generic_deleted").format(user.username)}, 200


class Users(Resource):

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help = 'This field cannot be blank', required = True)
        parser.add_argument('password', help = 'This field cannot be blank', required = True)
        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'. format(data['username'])}

        new_user = UserModel(
            username = data['username'],
            password = UserModel.generate_hash(data['password'])
        )
        try:
            new_user.save()
            return { 'message': 'User {} was created'.format( data['username']) }
        except Exception as e:
            return {'message': 'Something went wrong'}, 500

    @jwt_required
    def get(self):
        return UserModel.return_all()
    
    @jwt_required
    def delete(self):
        return UserModel.delete_all()