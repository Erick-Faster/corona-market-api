import sqlite3
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)

from blacklist import BLACKLIST
from models.user import UserModel
from models.userinfo import UserInfoModel

#_user_ -> private

_user_parser = reqparse.RequestParser()                        
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be blank")
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be blank")

_login_parser = reqparse.RequestParser()
_login_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be blank")
_login_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be blank")

class UserRegister(Resource):

    def post(self):

        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 400

        user = UserModel(**data) # = **data = data['username'], data['password']
        user.save_to_db()

        return user.json(), 201

class User(Resource):

    @classmethod
    def get(cls,user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return{'message': 'User deleted'}

class CurrentUser(Resource):

    @jwt_required
    def get(self):
        try:
            user_id = get_jwt_identity()
        except:
            return{'message': "Auth verification Failed"}

        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user.json()

class UserLogin(Resource):

    @classmethod
    def post(cls):

        data = _login_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return{
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'Invalid credentials'}, 401

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti'] #jti -> id do token
        BLACKLIST.add(jti)
        return {'message': "Successfully logged out"}

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
