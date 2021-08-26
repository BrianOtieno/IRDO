from flask import json, request, jsonify, abort, make_response
from flask_restful import Resource, Api 
from urllib.parse import quote, unquote
from IRDO.assets import blueprint 
from IRDO import db 
from .models import (
    Assets, asset_schema, assets_schema, 
    AssetTracking, tracking_schema, trackings_schema
)

from IRDO.users.models import User


api = Api(blueprint)

class Asset(Resource):
    
    def post(self):
        request_content = request.get_json() 
        itemname = request_content['itemname']
        itemcategory = request_content['itemcategory']
        itembarcode = request_content['itembarcode']  
        serialnumber = request_content['serialnumber']  
        itemprice = request_content['itemprice'] 
        itemlocation = request_content['itemlocation'] 

        if (itembarcode is None or itemname is None):
            abort(400) # missing arguments

        if Assets.query.filter_by(itembarcode = itembarcode).first() is not None:
            abort(409) # barcode not unique

        new_asset = Assets(itemname=itemname, itemcategory=itemcategory, 
        itembarcode=itembarcode, serialnumber=serialnumber, itemprice=itemprice, 
        itemlocation=itemlocation)

        db.session.add(new_asset)
        try:
            db.session.commit()
            return asset_schema.dump(new_asset), 201
        except:
            return {"msg": "Database error occured"}, 400 

    def get(self, itembarcode=None):
        if itembarcode is None:
            assets = Assets.query.all() 
            return assets_schema.dump(assets), 200
        else: 
            # itembarcode =  itembarcode[:4] + '/' + itembarcode[4:]
            itembarcode = itembarcode.replace('~', '/') 
            print(itembarcode)
            asset = db.session.query(Assets).filter(Assets.itembarcode.like("%"+itembarcode+"%")) 
            return assets_schema.dump(asset), 200
    
    def delete(self, id): 
        pass
    def update(self, id):
        pass

api.add_resource(Asset, '/') 
api.add_resource(Asset, '/<itembarcode>', methods=['GET'], endpoint='getassets')

class TrackAsset(Resource):

    def post(self):
        request_content = request.get_json() 
        username = request_content['username']
        itembarcode = request_content['itembarcode']
        assigned_by = request_content['assigned_by']   

        if (itembarcode is None or username is None):
            abort(400) # missing arguments

        if Assets.query.filter_by(itembarcode = itembarcode).first() is None:
            # data = {'msg':'barcode not in database'}
            # return make_response(jsonify(data), 406) # barcode not in database
            abort(406)
        
        if User.query.filter_by(username = username).first() is None:
            # data = {'msg':'user not in database'}
            # return make_response(jsonify(data), 409) # user not in database
            abort(409)
        
        asset = AssetTracking(username=username, itembarcode=itembarcode,
        assigned_by=assigned_by)

        db.session.add(asset)

        try:
            db.session.commit()
            # return asset_schema.dump(asset), 201
            return {"msg": "{itembarcode} Assigned!"}, 201
        except:
            return {"msg": "Database error occured"}, 400 
    
    def get(self, itembarcode):
        print(itembarcode)
        if itembarcode is None:
            assets = AssetTracking.query.all() 
            return trackings_schema.dump(assets), 200
        else: 
            asset = db.session.query(Assets).filter(Assets.itembarcode.like("%"+itembarcode+"%")) 
            return tracking_schema.dump(asset), 200

api.add_resource(TrackAsset, '/assign') 
api.add_resource(TrackAsset, '/get/<itembarcode>', methods=['GET'], endpoint='assign')