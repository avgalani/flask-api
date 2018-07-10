__author__ = 'Alex Galani'
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore, Security
from flask_marshmallow import Marshmallow
from App import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
ma = Marshmallow(app)

from App.models import User, Role, roles_users, Service, services_users
from App.routes import api

# Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security().init_app(app, user_datastore, register_blueprint=False)

default_services = [
    ("applejack","{'name': 'site1.com','region': 'nyc3','size':'512mb','image': 'ubuntu-14-04-x64','ssh_keys': None,'backups':False,'ipv6': False,'user_data': None,'private_networking':None,'volumes': None,'tags': ['frontend']}"),
    ("Fluttershy","{'name': 'example.com','region': 'nyc3','size':'512mb','image': 'ubuntu-16-04-x64','ssh_keys': None,'backups':False,'ipv6': true,'user_data': None,'private_networking': None,'volumes': None,'tags': ['frontend']}"),
    ("Rainbow Dash","{'name': 'backend01','region': 'nyc3','size':'512mb','image': 'centos 7.0','ssh_keys': None,'backups': False,'ipv6':true,'user_data': None,'private_networking': None,'volumes':None,'tags': ['backend']}"),
    ("Rarity","{'name': 'backend02','region': 'nyc3','size': '1GB','image':'centos 7.0','ssh_keys': None,'backups': False,'ipv6':False,'user_data': None,'private_networking': None,'volumes':None,'tags': ['web']}"),
    ("Pinkie Pie","{'name': 'db01','region': 'nyc3','size': '2GB','image':'centos 7.0','ssh_keys': None,'backups': False,'ipv6': true,'user_data':None,'private_networking': None,'volumes': None,'tags': ['web']}"),
    ("Alex Tema","{'name': 'test1','region': 'nyc4','size': '128KB','image': 'for-the-horde-x64','ssh_keys': None,'backups': False,'ipv6':False,'user_data': None,'private_networking': None,'volumes':None,'tags': ['test']}")]

default_users = ["nedstark@doe.john", "kaimelannister@doe.john", "cerseilannister@doe.john", "daeneristargaryen@doe.john", "littlefinger@doe.john", "jonsnow@doe.john", "alexBO$$@doe.john"]

# init database data
try:
    db.create_all()
    for user in default_users:
        db.session.add(User(user, 'password'))
    db.session.add(Role('admin', 'Can Create/Delete Users and Services'))
    db.session.add(Role('user', 'Can Create Services'))
    db.session.add(Role('automation', 'Can Delete Services'))
    for element in default_services:
        db.session.add(Service(element[0],element[1]))
    db.session.commit()
    db.engine.execute(roles_users.insert(), user_id=1, role_id=1)
    db.session.commit()
except:
    pass