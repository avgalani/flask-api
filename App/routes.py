
__author__ = 'responsible'
from App import app
from flask_restful import Api
from App.controller import Login, Users, Services, Roles

api = Api(app, default_mediatype="application/json")
api.add_resource(Users, '/users', '/users/add', '/users/<id>')
api.add_resource(Services, '/services', '/services/add', '/services/<id>')
api.add_resource(Login, '/login')
api.add_resource(Roles, '/roles')