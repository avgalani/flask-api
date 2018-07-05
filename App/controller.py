__author__ = 'responsible'
from flask_restful import Resource, reqparse
from flask_security import auth_token_required, roles_required, login_user
from passlib.handlers.django import django_pbkdf2_sha256
from .models import User, Service
from App import ma, jsonify, request, db


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('username', 'password')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class ServiceSchema(ma.Schema):
    class Meta:
        fields = ('name','properties')

service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)

class Protected(Resource):
    @auth_token_required
    def get(self):
        return {"msg": "pl"}, 200

    @auth_token_required
    @roles_required('admin')  
    def post(self):
        return {"msg": "okay"}, 201


class Login(Resource): 
    def post(self):
        args = reqparse.RequestParser() \
            .add_argument('username', type=str, location='json', required=True, help="hh") \
            .add_argument("password", type=str, location='json', required=True, help="ohk") \
            .parse_args()
        user = User.authenticate(args['username'], args['password'])
        if user:
            login_user(user=user)
            return {"message": "okk", "token": user.get_auth_token()}, 200
        else:
            return {"message": "nok"}, 401

class Users(Resource):
    @auth_token_required
    @roles_required('admin')
    def post(self):
        username = request.json['username']
        password = django_pbkdf2_sha256.encrypt(request.json['password'])
        print(password)
        new_user = User(username, password)
        result = user_schema.dump(new_user, False)
        try: 
            db.session.add(new_user)
            db.session.commit()
        except:
            db.session.rollback()
            return "Did not succeed"
        return (username + " created")
            

    @auth_token_required
    def get(self):
        all_users = User.query.all()
        result = users_schema.dump(all_users)
        return jsonify(result.data)

class Services(Resource):
    def get(self):
        all_services = Service.query.all()
        result = services_schema.dump(all_services)
        return jsonify(result.data)