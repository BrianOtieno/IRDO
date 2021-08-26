from flask import json, request, jsonify, abort, make_response
from flask_restful import Resource, Api 
from urllib.parse import quote, unquote

from marshmallow.fields import DateTime
from IRDO.attendance import blueprint 
from IRDO import db 
from .models import (
    Attendance, attendance_schema, attendances_schema
)

from IRDO.users.models import User

api = Api(blueprint)

class Timesheet(Resource):
    
    def post(self):
        request_content = request.get_json() 
        username = request_content['username']
        authorized_by = request_content['authorized_by']
        # time = DateTime.utcnow()   

        if (username is None or authorized_by is None):
            abort(400) # missing arguments

        if User.query.filter_by(username = username).first() is None:
            abort(409) # user not in database
        
        if User.query.filter_by(username = username).first() is None:
            abort(409) # user not in database

        new_attendance = Attendance(username=username, authorized_by=authorized_by)

        db.session.add(new_attendance)
        try:
            db.session.commit()
            return attendance_schema.dump(new_attendance), 201
        except:
            return {"msg": "Database error occured"}, 400 

    def get(self, username=None):
        if username is None:
            attendance = Attendance.query.all() 
            return attendances_schema.dump(attendance), 200
        else: 
            # username =  username[:4] + '/' + username[4:]
            username = username.replace('~', '/')  
            attendance = db.session.query(Attendance).filter(
                Attendance.username.like("%"+username+"%")) 
            return attendances_schema.dump(attendance), 200
    
    def delete(self, id): 
        pass
 
api.add_resource(Timesheet, '/', methods=['GET','POST'], endpoint='timesheet')
 