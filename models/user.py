import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))

    userinfos = db.relationship('UserInfoModel', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'message': 'User created successfully!'}
    
    @property #Transforma atributo em private qdo alguem chamar por self.id
    def get_id(self):
         return self._id

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
