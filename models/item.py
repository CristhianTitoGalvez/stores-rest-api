import sqlite3
from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self,name,price,store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name':self.name, 'price':self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # .query comes from SQLALchemy (db.Model)- Equal to "SELECT * FROM items WHERE name=name LIMIT 1"
        # this returns an ItemModel object 
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        connection.close()

        if row is not None:
            return cls(row[0], row[1]) #or (*row). This returns an object
        return None 
        """
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        #SQLAlchemy translates from object to row in a DB
        #this method executes insert and update

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        