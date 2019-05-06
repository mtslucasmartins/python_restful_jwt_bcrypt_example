from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, 
    jwt_refresh_token_required, get_jwt_identity, get_raw_jwt
)

from libs.strings import gettext
from models.user import UserModel


class User(Resource):

    @jwt_required
    def get(self, id):
        current_user = UserModel.find_by_email(get_jwt_identity())
        user = UserModel.find_by_id(id, current_user)
        if not user:
            return { 'message': gettext("user_not_found") }, 404
        return user.json(), 200

    @jwt_required
    def delete(self, id: str):
        current_user = UserModel.find_by_email(get_jwt_identity())
        deleted_user = UserModel.find_by_id(id, current_user)

        if not user:
            return {'status': 'error', 'message': gettext("user_not_found")}, 404
        user.delete()
        return {'status': 'success', 'message': gettext("generic_deleted").format(user.username)}, 200


class Users(Resource):

    @jwt_required
    def post(self):
        current_user =  UserModel.find_by_email(get_jwt_identity())

        request_parser = reqparse.RequestParser()    
        request_parser.add_argument('email', help='This field cannot be blank', required=True)
        request_parser.add_argument('fullname', help='This field cannot be blank', required=True)
        request_parser.add_argument('password', help='This field cannot be blank', required=True)
        request_args = request_parser.parse_args()

        user = UserModel(
            email = request_args.get('email'), 
            fullname = request_args.get('fullname'),
            username = request_args.get('email'),
            password = UserModel.generate_hash(request_args.get('password')),
            clinic = current_user.clinic
        )

        if UserModel.find_by_email(user.username):
            return {'status': 'error', 'message': 'User {} already exists'. format(user.username)}, 500

        try:
            user.save()

            record = user

            return {'status': 'success', 'record': user.json() }
        except Exception as e:
            return {'status': 'error', 'message': 'Something went wrong'}, 500

    @jwt_required
    def get(self):
        current_user = UserModel.find_by_email(get_jwt_identity())

        page_index = int(request.args.get('page_index', 0))
        page_size = int(request.args.get('page_size', 10))
        
        count = UserModel.count_all(authorized_user=current_user)
        users = UserModel.find_all(offset=page_index*page_size, limit=page_size, authorized_user=current_user)
        
        return {
            'status': 'success', 
            'records': [ user.json() for user in users ], 
            'length': count,
            'page_index': page_index,
            'page_size': page_size
        }
    
    @jwt_required
    def delete(self):
        return UserModel.delete_all()