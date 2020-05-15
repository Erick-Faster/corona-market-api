from db import db
from flask_jwt_extended import get_jwt_identity
from datetime import datetime
from json import dumps

class RequestModel(db.Model):
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    address = db.Column(db.String(80))
    author = db.Column(db.String(20))
    accepted = db.Column(db.String(3))
    done = db.Column(db.String(3))
    date_posted = db.Column(db.String())

    userinfo_id = db.Column(db.Integer, db.ForeignKey('usersinfo.id'))
    userinfo = db.relationship('UserInfoModel')

    items = db.relationship('ItemModel', lazy='dynamic') #retorna lista // lazy=dynamic -> nao cria um objeto pra cada item. 

    def __init__(self, name, address, author, accepted, done):
        self.name = name
        self.address = address
        self.author = author
        self.accepted = accepted
        self.done = done
        self.userinfo_id = get_jwt_identity()
        self.date_posted = str(datetime.now().strftime("%x às %X"))

    def json(self):
        return {
            'id': self.id,
            'userinfo_id': self.userinfo_id,
            'name': self.name,
            'address': self.address,
            'author': self.author,
            'accepted': self.accepted,
            'done': self.done,
            'date_posted': self.date_posted,
            'items': [item.json() for item in self.items.all()] #all() para n crashar o lazy
            }

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first() #posso colocar varios filter_by 

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first() #posso colocar varios filter_by

    @classmethod
    def find_by_user_id(cls,user_id):
        return cls.query.filter_by(userinfo_id=user_id)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()