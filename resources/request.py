from flask_restful import Resource, reqparse
from models.request import RequestModel
from flask_jwt_extended import jwt_required, get_jwt_identity

_request_parser = reqparse.RequestParser()
_request_parser.add_argument('name',
    type=str,
    required=True,
    help="This field cannot be left blank!"
)
_request_parser.add_argument('address',
    type=str,
    required=True,
    help="This field cannot be left blank!"
)
_request_parser.add_argument('author',
    type=str,
    required=True,
    help="Every request needs a request_id"
)
_request_parser.add_argument('accepted',
    type=str,
    required=True,
    help="This field cannot be left blank!"
)
_request_parser.add_argument('done',
    type=str,
    required=True,
    help="This field cannot be left blank!"
)


class Request(Resource):

    def get(self, id):
        request = RequestModel.find_by_id(id)
        if request:
            return request.json()
        return {'message': 'request not found'}, 404

    def put(self,id):
        data = _request_parser.parse_args() #Validacao das condicoes de entrada

        request = RequestModel.find_by_id(id)
        
        if request:            
            request.name = data['name']
            request.address = data['address']
            request.author = data['author']
            request.accepted = data['accepted']
            request.done = data['done']
        else:
            return {'message': 'Request not found'}, 404
        
        request.save_to_db()
        return request.json()

    def delete(self, id):
        request = RequestModel.find_by_id(id)
        if request:
            request.delete_from_db()

        return {'message': 'Request deleted'}


class NewRequest(Resource):

    @jwt_required
    def post(self):

        data = _request_parser.parse_args() #Validacao das condicoes de entrada

        if RequestModel.find_by_name(data['name']):
            return {'message': "A Request with name '{}' already exists".format(data['name'])}, 400

        request = RequestModel(**data)

        try:
            request.save_to_db()
        except:
            return {'message': "An error occured while creating the request"}, 500

        return request.json(), 201

class RequestList(Resource):
    def get(self):
        return [request.json() for request in RequestModel.find_all()]

class RequestUsers(Resource):

    @jwt_required
    def get(self):
        user_id = get_jwt_identity() 
        return [request.json() for request in RequestModel.find_by_user_id(user_id)]
