from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
#import sqlite3
from models.item import ItemModel

#Apis work with resources and every resource is a class. Below the "Item" class inherits Resource class.
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float, 
        required=True, 
        help="This field cannot be left blank"
    )

    parser.add_argument('store_id', 
    type=int, 
    required=True, 
    help="Every item needs a store ID"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item is not None:
            return item.json() 
        return {'message': 'Item not found.'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name) is not None:
            return {'message':'An item with name {} already exists'.format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()
        except:
            return {'message':'An error occurred inserting the item.'}, 500 # internal server error

        return item.json(), 201 #201 status code is "Created"

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            #ItemModel.delete_from_db(item)

        return {'message': 'Item deleted'}

    def put(self,name):
        data = Item.parser.parse_args() # It is gonna parse the arguments that come through the JSON payload and is gonna put the valid ones in data as defined! 
        
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])

        else:
            item.price = data['price']
        
        item.save_to_db()

        return item.json()

class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items=[]
        for row in result:
            items.append({'name':row[0], 'price':row[1]})
        
        connection.commit()
        connection.close()
        """
        return {'items':items}

