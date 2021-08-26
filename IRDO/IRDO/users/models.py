from enum import unique
from operator import is_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from IRDO import db, ma 
from ..base.models import BaseModel
import uuid

class User(db.Model):
    __tablename__ = 'appusers' 
    uid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    middlename = db.Column(db.String(50))
    lastname = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(150),nullable=False)
    phonenumber = db.Column(db.String(15))
    email = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(256))
    public_key = db.Column(db.String(64))
    is_active = db.Column(db.Boolean, unique=False, default=False)

    def __init__(self, firstname, middlename, lastname, department, phonenumber,
    email, username, password, public_key, is_active):
        self.firstname = firstname.title()
        self.middlename = middlename.title()
        self.lastname = lastname.title()
        self.department = department
        self.phonenumber = phonenumber
        self.email = email.lower()
        self.username = username.lower()
        self.set_password(password)
        self.public_key = public_key
        self.is_active = is_active
        # self.password = password

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# users schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('uid', 'firstname', 'middlename', 'lastname', 'phonenumber',
         'username', 'email')

# initialize user schema 
user_schema = UserSchema()
users_schema = UserSchema(many=True) 

    