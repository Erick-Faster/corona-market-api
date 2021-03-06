from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, fresh_jwt_required, get_jwt_claims, get_jwt_identity, jwt_optional
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser() #Condicoes de entrada

    parser.add_argument('quantity',
        type=int,
        required=True,
        help="Every request needs a quantity"
    )
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('request_id',
        type=int,
        required=True,
        help="Every request needs a request_id"
    )

    @jwt_required #JWT_extended N TEM ()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @fresh_jwt_required
    def post(self, name):

        data = Item.parser.parse_args() #Validacao das condicoes de entrada
        
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occured inserting the item"}, 500

        return item.json(), 201

    @jwt_required
    def delete(self, name):

        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required'}, 401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}
        
    @jwt_required
    def put(self,name):
        data = Item.parser.parse_args() #Validacao das condicoes de entrada

        item = ItemModel.find_by_name(name)
        
        if item:
            item.price = data['price']
            item.quantity = data['quantity']
        else:
            item = ItemModel(name, **data)
        
        item.save_to_db()
        return item.json()


class ItemList(Resource):

    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {'items': items}, 200
        return {
            'items': [item['name'] for item in items],
            'message': 'More data avaliable if you log in'}, 200
        
        

        #return {'items': list(map(lambda x: x.json(), ItemModel.find_all()))} #[item.json() for item in ItemModel.query.all()
