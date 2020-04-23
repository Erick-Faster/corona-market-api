import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(20))

    requests = db.relationship('RequestModel', lazy='dynamic')

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod #Indica metodo da classe
    def find_by_username(cls,username):
        return cls.query.filter_by(username=username).first()

    @classmethod #Indica metodo da classe
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()
