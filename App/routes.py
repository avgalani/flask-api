
__author__ = 'responsible'
from App import app
from flask_restful import Api
from App.controller import Protected, Login, Users

api = Api(app, default_mediatype="application/json")
api.add_resource(Users, '/users')
api.add_resource(Login, '/login')
api.add_resource(Protected, '/protected')