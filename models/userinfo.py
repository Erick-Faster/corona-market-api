import sqlite3
from db import db

class UserInfoModel(db.Model):
    __tablename__ = 'usersinfo'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    group = db.Column(db.String(20))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')

    requests = db.relationship('RequestModel', lazy='dynamic')


    def __init__(self, username, name, email, group, user_id):
        self.username = username
        self.name = name
        self.email = email
        self.group = group
        self.user_id = user_id

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'group': self.group,
            'user_id': self.user_id
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod #Indica metodo da classe
    def find_by_username(cls,username):
        return cls.query.filter_by(username=username).first()

    @classmethod #Indica metodo da classe
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()