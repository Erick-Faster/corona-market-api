from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.userinfo import UserInfoModel
from models.user import UserModel



class UserInfo(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                            type=str,
                            required=True,
                            help="This field cannot be blank")
    parser.add_argument('name',
                            type=str,
                            required=True,
                            help="This field cannot be blank")
    parser.add_argument('email',
                            type=str,
                            required=True,
                            help="This field cannot be blank")                          
    parser.add_argument('group',
                            type=str,
                            required=True,
                            help="This field cannot be blank")
    parser.add_argument('user_id',
                            type=int,
                            required=True,
                            help="This field cannot be blank")

    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        userinfo = UserInfoModel.find_by_id(user_id)
        if userinfo:
            return userinfo.json()
        return {'message':'User not found'}, 400
        
    def post(self):

        data = UserInfo.parser.parse_args() #Validacao das condicoes de entrada

        if not UserModel.find_by_username(data['username']):
            return {'message': "Account does not exists"}, 400
        
        userinfo = UserInfoModel(**data)

        try:
            userinfo.save_to_db()
        except:
            return {"message": "An error occured while inserting the item"}, 500

        return userinfo.json(), 201

class UserInfos(Resource):
    def get(self):
        return [userinfo.json() for userinfo in UserInfoModel.find_all()]
