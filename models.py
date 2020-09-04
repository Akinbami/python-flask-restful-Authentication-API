from flask_migrate import Migrate, MigrateCommand
from flask_marshmallow import Marshmallow

from passlib.hash import pbkdf2_sha256 as sha256

from datetime import timedelta, datetime as dt
import datetime
import random

from app import app,db

ma = Marshmallow(app)
migrate = Migrate(app,db)

# Defining user model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(500))
    date_registered = db.Column(db.DateTime, nullable=False, default=str(dt.today()))
    date_updated = db.Column(db.DateTime, nullable=False, default=str(dt.today()))


    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
        
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return user_schema.dump(self)

    def update_db(self):
        db.session.commit()
        return user_schema.dump(self)

    @classmethod
    def find_by_username(cls, username):
       return cls.query.filter_by(username = username).first()


    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
	            'username': x.username,
	            'password': x.password
            }
        return {'users': list(map(lambda x: to_json(x), User.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

# Define model to manage revoked tokens
class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', "date_registered")




user_schema = UserSchema()
users_schema = UserSchema(many=True)