from flask import Flask
from flask_restful import reqparse, Api, Resource

app = Flask(__name__)
api = Api(app)

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument()

    def Post(self, name):
        data = Item.parser.parse_args()

        newitem = {'name' = data['name']}
        item.append(newitem)
        return newitem, 201


api.add_resource(Items,'/item')
app.run()