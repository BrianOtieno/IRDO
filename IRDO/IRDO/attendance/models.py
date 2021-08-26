from marshmallow import fields
from IRDO import db, ma  
from ..base.models import BaseModel
import datetime
from sqlalchemy import DateTime

class Attendance(db.Model):
    __tablename__ = 'attendance' 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), 
    db.ForeignKey('appusers.username', onupdate="cascade"))
    authorized_by = db.Column(db.String(100), 
    db.ForeignKey('appusers.username', onupdate="cascade"))
    time = db.Column(db.DateTime(timezone=True, ), nullable=True, default=datetime.datetime.utcnow) 
    # time = db.Column(DateTime, default=datetime.datetime.utcnow)
  

    def __init__(self, username, authorized_by):
        self.username = username
        self.authorized_by = authorized_by 

# attendance schema
class AttendanceSchema(ma.Schema):
    class Meta:
        fields = ('username', 'authorized_by', 'time')

# initialize attendance schema 
attendance_schema = AttendanceSchema()
attendances_schema = AttendanceSchema(many=True) 
 