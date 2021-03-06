from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy = 'dynamic')

    def __init__(self,name):
        self.name = name

    def json(self):
        return {'name':self.name, 'items':[item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # .query comes from SQLALchemy (db.Model)- Equal to "SELECT * FROM items WHERE name=name LIMIT 1"
        # this returns an ItemModel object 

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        #SQLAlchemy translates from object to row in a DB
        #this method executes insert and update

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        