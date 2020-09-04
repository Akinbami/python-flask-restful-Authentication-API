from flask import request,make_response,jsonify
from flask_restful import Resource,reqparse,abort
from flask_jwt_extended import (create_access_token, 
                                create_refresh_token, 
                                jwt_required, 
                                jwt_refresh_token_required, 
                                get_jwt_identity, 
                                get_raw_jwt
                            )
from sqlalchemy.orm.exc import NoResultFound

from datetime import timedelta, datetime
import uuid
import logging

from models import User,user_schema,RevokedTokenModel


def abort_if_user_doesnt_exist(id):
    user = User.get_one(id)
    if not user:
        abort(404, message="User {} doesn't exist".format(id))

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        password = User.generate_hash(data['password'])

        # creating the user instance
        new_user = User(username=data['username'],password=password)
        user = new_user.save_to_db()

        return {"status": "Ok","data":user}

    def get(self):
        return {'hello': 'world'}

class UserLogin(Resource):
    def post(self):
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return make_response("Could not verify", 401, {'WWW-Authenticate': 'Basic realm="Login Required!'})

        user = User.query.filter_by(username=auth.username).first()
        if not user:
            return make_response("Could not verify", 401, {'WWW-Authenticate': 'Basic realm="Login Required!'})

        verify_user = User.verify_hash(auth.password,user.password)
        if verify_user:
            expires = timedelta(days=7)
            access_token = create_access_token(identity = auth.username,expires_delta=expires)
            refresh_token = create_refresh_token(identity = auth.username)
            return {
                'status': verify_user,
                'message': 'Logged in as {}'.format(user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        else:
            return {'message': 'Wrong credentials',"status": verify_user}

     
class UserLogoutAccess(Resource):
    @jwt_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500
        


# User page authorization
class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'valid': True
        }
 