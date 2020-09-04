from flask import Flask

from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager




import json

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root@localhost:3306/flask_auth"
app.config["JWT_SECRET_KEY"] = "gfhjvbknmkkhbjghfgchgjbk637uhgfsghj2iuj"
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = dt.now() + timedelta(days = 1)
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=1)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)


CORS(app)

# Using the expired_token_loader decorator, we will now call
# this function whenever an expired but otherwise valid access
# token attempts to access an endpoint

import models, resources

@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'The {} token has expired'.format(token_type)
    }), 401
    
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    print("checking blacklist")
    return models.RevokedTokenModel.is_jti_blacklisted(jti)


@jwt.revoked_token_loader
def revoked_token_response(revoked_token):
    token_type = revoked_token['type']
    jwtkn = revoked_token['jti']
    print("checking if token is revoked blacklist")
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'The {} token has expired'.format(token_type)
    }), 401

api.add_resource(resources.UserRegistration, '/api/register')
api.add_resource(resources.UserLogin, '/api/login')
api.add_resource(resources.UserLogoutAccess, '/api/logout/access')
# api.add_resource(resources.UserLogoutRefresh, '/api/logout/refresh')
# api.add_resource(resources.TokenRefresh, '/api/token/refresh')
api.add_resource(resources.UserList, '/api/users')
api.add_resource(resources.UserDetail, '/api/users/<public_id>')
api.add_resource(resources.SecretResource, '/api/secret')




