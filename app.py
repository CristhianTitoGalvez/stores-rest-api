from security import authenticate, identity
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.user import UserRegister
from resources.item import Item, ItemList
from db import db
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #Here we say that the SQLAlchemy data.db is gonna live at the root folder of my project
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # turns off the flask SQLALchemy modification tracker because the library itself come with this feature
app.secret_key = 'jose'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity) # jwt creates a new endpoint: /auth. When we call /auth it send username and pass.


api.add_resource(Item, '/item/<string:name>') 
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

#The file one runs is '__main__'. If it is not main it means that we have imported the file from elsewhere
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)