from flask import json, request, jsonify, abort, make_response
from flask_restful import Resource, Api
from marshmallow.fields import UUID
from IRDO.users import blueprint
from .models import User
from IRDO import db
from .models import user_schema , users_schema

api = Api(blueprint)

class Users(Resource):
    def post(self):
        request_content = request.get_json()
        firstname = request_content['firstname']
        middlename = request_content['middlename']
        lastname = request_content['lastname']
        department = request_content['department']
        phonenumber = request_content['phonenumber']
        email = request_content['email']
        username = request_content['email']
        password = request_content['password'] 
        public_key = None
        is_active = False

        if (username is None or password is None or firstname is None or 
        lastname is None or email is None):
            abort(400) # missing arguments
        
        if User.query.filter_by(username = username).first() is not None:
            abort(400) # existing user

        new_user = User(firstname=firstname, middlename=middlename, 
        lastname=lastname, department=department, phonenumber=phonenumber, 
        email=email, username=username, password=password, 
        public_key=public_key, is_active=is_active)

        db.session.add(new_user)
        try:
            db.session.commit()
            return user_schema.dump(new_user), 201
        except:
            return {"msg": "Error. Check if user exist"}, 400 
    def get(self, username):
        print(username)
        if username is None:
            users = User.query.all() 
            return users_schema.dump(users), 200
        else: 
            asset = db.session.query(User).filter(User.username.like("%"+username+"%")) 
            return users_schema.dump(asset), 200

class UserLogin(Resource):
    def post(self):
        request_content = request.get_json()
        username = request_content['username']
        password = request_content['password'] 

        if username is None or password is None:
            abort(400) # missing arguments

        user = User.query.filter_by(username = username).first()
        if not user or not user.check_password(password):
            abort(403) # User not found and cant be authenticated 
        
        firstname = user.firstname
        lastname = user.lastname
        email = user.email
        data = {'username': username, 'firstname': firstname, 
        'lastname':lastname, 'email': email}
        return make_response(jsonify(data), 200)

class Home(Resource):
    def get(self):
        return {
            'HOME': 'IRDO API',
            'API Version': 'Version 001'
        }


class Employees(Resource):
    def get(self):
        return {
            'name' : 'Brian Otieno',
            'Depertment': 'SI'
        }


api.add_resource(Users, '/', methods=['GET', 'POST'])
api.add_resource(Users, '/<username>', methods=['GET'], endpoint='get_user')
api.add_resource(UserLogin, '/login')
api.add_resource(Employees, '/employees') 
