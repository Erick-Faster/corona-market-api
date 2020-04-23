import sqlite3
from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    quantity = db.Column(db.Integer())
    price = db.Column(db.Float(precision=2))


    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'))
    request = db.relationship('RequestModel')

    def __init__(self, name, quantity, price, request_id):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.request_id = request_id

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity,
            'price': self.price,
            'request_id': self.request_id
        }

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first() #posso colocar varios filter_by 

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()