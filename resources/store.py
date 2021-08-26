from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store is not None:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self,name):
        if StoreModel.find_by_name(name):
            return {'message': "Store '{}'' is already there.".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message':'Error ocurred while creating store.'}, 500
        
        return store.json(), 201

    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store is not None:
            store.delete_from_db()
            #StoreModel.delete_from_db(store)

        return {'message':'Store deleted'}
        
class StoreList(Resource):
    def get(self):
        return {'stores':[store.json() for store in StoreModel.query.all()]}

