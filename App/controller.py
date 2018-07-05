__author__ = 'responsible'
from flask_restful import Resource, reqparse
from flask_security import auth_token_required, roles_required, login_user
from .models import User
from App import ma, jsonify


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('username', 'password')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


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
    def get(self):
        all_users = User.query.all()
        result = users_schema.dump(all_users)
        return jsonify(result.data)
