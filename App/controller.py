__author__ = 'Alex Galani'

from flask_restful import Resource, reqparse
from flask_security import auth_token_required, roles_required, login_user, roles_accepted
from passlib.handlers.django import django_pbkdf2_sha256
from .models import User, Service, Role, roles_users
from App import ma, jsonify, request, db


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('username', 'password')

class ServiceSchema(ma.Schema):
    class Meta:
        fields = ('name','properties')

class RoleSchema(ma.Schema):
    class Meta:
        fields = ('name', 'description')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)
role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)

class Login(Resource): 
    def post(self):
        args = reqparse.RequestParser() \
            .add_argument('username', type=str, location='json', required=True) \
            .add_argument("password", type=str, location='json', required=True) \
            .parse_args()
        user = User.authenticate(args['username'], args['password'])
        if user:
            login_user(user=user)
            return {"message": "login succeeded", "token": user.get_auth_token()}, 200
        else:
            return {"message": "nok", "user": args}, 401

class Users(Resource):
    @auth_token_required
    @roles_required('admin')
    def post(self, id = None):
        username = request.json['username']
        password = request.json['password']
        if id:
            role_id = request.json['role_id']
            statement = roles_users.insert().values(user_id=id,role_id=role_id)
            db.session.execute(statement)
            db.session.commit()
        else:
            new_user = User(username, password)
            # result = user_schema.dump(new_user, False)
            try: 
                db.session.add(new_user)
                db.session.commit()
            except:
                db.session.rollback()
                return "Did not succeed"
            return (username + " created")
            

    
    def get(self, id = None):
        if id:
            user = User.query.get(id)
            result = user_schema.dump(user)
            return jsonify(result.data['username'])
        else:
            all_users = User.query.all()
            result = users_schema.dump(all_users)
            return jsonify(result.data)

class Services(Resource):
    @auth_token_required
    def get(self, id = None):
        if id:
            service = Service.query.get(id)
            result = service_schema.dump(service)
            return jsonify(result.data)
        else:
            all_services = Service.query.all()
            result = services_schema.dump(all_services)
            return jsonify(result.data)

    @auth_token_required
    @roles_accepted('admin','user')
    def post(self):
        name = request.json['name']
        properties = str(request.json['properties'])
        new_service = Service(name, properties)
        result = service_schema.dump(new_service, False)
        try:
            db.session.add(new_service)
            db.session.commit()
        except:
            db.session.rollback()
            return "Did not succeed"
        return (name + " created and added to db")

    @auth_token_required
    @roles_accepted('admin','automation')
    def delete(self):
        ## TODO unhappy flows
        id = request.json['id']
        service = Service.query.filter_by(id=id).delete()
        db.session.commit()
        return "User has been succesfully deleted"        

class Roles(Resource):
    @auth_token_required
    def get(self):
        all_roles = Role.query.all()
        result = roles_schema.dump(all_roles)
        return jsonify(result.data)