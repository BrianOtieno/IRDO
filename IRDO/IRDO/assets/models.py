from marshmallow import fields
from IRDO import db, ma  
from ..base.models import BaseModel

class Assets(db.Model):
    __tablename__ = 'assets' 
    id = db.Column(db.Integer, primary_key=True)
    itemname = db.Column(db.String(250), nullable=False)
    itemcategory = db.Column(db.String(100), nullable=False)
    itembarcode = db.Column(db.String(50), unique=True, nullable=False) 
    serialnumber = db.Column(db.String(50), unique=True, nullable=False)
    itemprice = db.Column(db.Integer())
    itemlocation = db.Column(db.String(100)) 

    def __init__(self, itemname, itemcategory, itembarcode, serialnumber,
    itemprice, itemlocation):
        self.itemname = itemname
        self.itemcategory = itemcategory
        self.itembarcode = itembarcode
        self.serialnumber = serialnumber
        self.itemprice = itemprice 
        self.itemlocation = itemlocation

# users schema
class AssetsSchema(ma.Schema):
    class Meta:
        fields = ('itemname', 'itemcategory', 'itembarcode', 'serialnumber',
        'itemprice', 'itemlocation')

# initialize user schema 
asset_schema = AssetsSchema()
assets_schema = AssetsSchema(many=True) 


class AssetTracking(db.Model):
    __tablename__ = 'asset_tracking'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), 
    db.ForeignKey('appusers.username'))
    itembarcode = db.Column(db.String(50), 
    db.ForeignKey('assets.id'))
    assigned_by = db.Column(db.String(100), 
    db.ForeignKey('appusers.username', onupdate="cascade")) 

    def __init__(self, username, itembarcode, assigned_by):
        self.itembarcode = itembarcode
        self.username = username
        self.assigned_by = assigned_by


class AssetTrackingSchema(ma.Schema):
    class Meta:
        fields = ('username', 'itembarcode', 'assigned_by')


tracking_schema = AssetTrackingSchema()
trackings_schema = AssetTrackingSchema(many=True)