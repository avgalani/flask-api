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

from App.models import User, Role, roles_users, Service
from App.routes import api

# Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security().init_app(app, user_datastore, register_blueprint=False)

default_services =[
    ("applejack","{'name': 'site1.com','region': 'nyc3','size':'512mb','image': 'ubuntu-14-04-x64','ssh_keys': None,'backups':False,'ipv6': False,'user_data': None,'private_networking':None,'volumes': None,'tags': ['frontend']}"),
    ('Fluttershy','{"name": "example.com","region": "nyc3","size":"512mb","image": "ubuntu-16-04-x64","ssh_keys": None,"backups":False,"ipv6": true,"user_data": None,"private_networking": None,"volumes": None,"tags": ["frontend"]}'),
    ('Rainbow Dash','{"name": "backend01","region": "nyc3","size":"512mb","image": "centos 7.0","ssh_keys": None,"backups": False,"ipv6":true,"user_data": None,"private_networking": None,"volumes":None,"tags": ["backend"]}'),
    ('Rarity','{"name": "backend02","region": "nyc3","size": "1GB","image":"centos 7.0","ssh_keys": None,"backups": False,"ipv6":False,"user_data": None,"private_networking": None,"volumes":None,"tags": ["web"]}'),
    ('Pinkie Pie','{"name": "db01","region": "nyc3","size": "2GB","image":"centos 7.0","ssh_keys": None,"backups": False,"ipv6": true,"user_data":None,"private_networking": None,"volumes": None,"tags": ["web"]}')]



# init database data
try:
    db.create_all()
    db.session.add(User('nedstark@doe.john', 'password'))
    db.session.add(User('kaimelannister@doe.john', 'password'))
    db.session.add(User('cerseilannister@doe.john', 'password'))
    db.session.add(User('daeneristargaryen@doe.john', 'password'))
    db.session.add(User('littlefinger@doe.john', 'password'))
    db.session.add(User('jonsnow@doe.john', 'password'))
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