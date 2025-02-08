from flask import request,jsonify
from flask_restx import Resource,Namespace
from model_fields import signup_fields,login_fields
from flask_jwt_extended import JWTManager,create_access_token,create_refresh_token,jwt_required, get_jwt_identity, set_access_cookies, set_refresh_cookies, unset_jwt_cookies
from models import User
from werkzeug.security import generate_password_hash,check_password_hash
import json


auth_ns=Namespace('auth',description='Namespace for Authentication operations')
signup_model=auth_ns.model('Signup',signup_fields)
login_model=auth_ns.model('Login',login_fields)

@auth_ns.route('/signup')
class Signup(Resource):
    @auth_ns.expect(signup_model)
    def post(self):
        data=request.get_json()
        username=data.get('username')
        db_user=User.query.filter_by(username=username).first()
        if db_user is not None:
            return jsonify({'message':f'User with username {username} already exists'})
        new_user=User(
            username=data.get('username'),
            email=data.get('email'),
            password=generate_password_hash(data.get('password')),
            role=data.get('role')
        )
        new_user.save()
        return jsonify({"message":"User created successfully"})

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data=request.get_json()
        username=data.get('username')
        password=data.get('password')
        if not username or not password:
            return jsonify({"message":"Both username and password are required"})
        db_user=User.query.filter_by(username=username).first()
        if db_user and check_password_hash(db_user.password,password):
            user_identity=json.dumps({"username":db_user.username,
                                      "role":db_user.role
                                      })
            access_token=create_access_token(identity=user_identity)
            refresh_token=create_refresh_token(identity=user_identity)
            return jsonify({"access_token":access_token,"refresh_token":refresh_token})

