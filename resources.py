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

from models import User,user_schema


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
        blacklist.add(jti)
        return jsonify({"msg": "Successfully logged out"}), 200

class UserList(Resource):
    def get(self):
        return User.return_all()

class UserDetail(Resource):
    def get(self, id):
        abort_if_user_doesnt_exist(id)
        return User.get_one(id)

    def delete(self, id):
        abort_if_user_doesnt_exist(id)
        User.delete_one(id)
        return '', 204

    def patch(self, id):
        data = request.get_json()
        user = User.query.get_or_404(id)

        # updating post
        if "username" in data:
            user.username = data['username']
        if "email" in data:
            user.email = data['email']
        if "is_admin" in data:
            user.is_admin = data['is_admin']

        update_response = user.update_db()


        return update_response, 201

# User page authorization
class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'valid': True
        }
 