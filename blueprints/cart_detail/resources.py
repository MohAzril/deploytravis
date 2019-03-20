import logging, json
from flask import Blueprint, Flask, request
from flask_restful import Api, Resource, reqparse, marshal
from time import strftime 
from logging.handlers import RotatingFileHandler
from flask_jwt_extended import jwt_required, get_jwt_claims
import random
#add __init__.py
from . import *
from blueprints.item import *
from blueprints import db
from datetime import date, datetime

bp_cartdetail = Blueprint('cartdetail', __name__)
api = Api(bp_cartdetail)

class CartsDetailResource(Resource):

    def __init__(self):
        pass
    
    @jwt_required
    def get(self,cart_id,id=None):
        status = get_jwt_claims()['status']
        if status != "customer" and status != "admin":
            return {'message':'Only customer and admin'},404, { 'Content-Type': 'application/json' }
        if id is None:
            parser = reqparse.RequestParser()
            parser.add_argument('p',type=int, location='args', default=1)
            parser.add_argument('rp',type=int, location='args', default=5)
            parser.add_argument('id',type=int, location='args')
            parser.add_argument('nama_item', location='args')
            args = parser.parse_args()#sudah jadi dictionary    
            
            offset = (args['p'] * args['rp']) - args['rp']
            
            if status == "customer":
                qry = Cartdetail.query.filter_by(cart_id=cart_id)
            else:
                qry = Cartdetail.query

            if args['id'] is not None:
                qry = qry.filter_by(id=args['id'])
            if args['nama_item'] is not None:
                qry = qry.filter(Cartdetail.nama_item.like("%"+args['nama_item']+"%"))

            rows = [{'page':args['p']}]
            for row in qry.limit(args['rp']).offset(offset).all():
                temp = marshal(row, Cartdetail.respon_fields)
                rows.append(temp)

            return rows, 200, { 'Content-Type': 'application/json' }
        else :
            customer_id = get_jwt_claims()['user_id']
            if status == "customer":
                qry = Cartdetail.query.filter_by(cart_id=cart_id).filter_by(id=id).first()
            else:
                qry = Cartdetail.query.filter_by(id=id).first()
            
            if qry is not None:
                temp = marshal(qry, Cartdetail.respon_fields)
                return temp, 200, { 'Content-Type': 'application/json' }
            return {'status': 'NOT_FOUND','message':'item not found'},404, { 'Content-Type': 'application/json' }
    
    @jwt_required
    def post(self,cart_id):
        status = get_jwt_claims()['status']
        if status != "customer":
            return {'message':'Only customer can post cart detail'},404, { 'Content-Type': 'application/json' }
        parser = reqparse.RequestParser()
        parser.add_argument('item_id', location='json', type=int, required=True)
        parser.add_argument('qty', location='json', type=int, required=True)
        args = parser.parse_args()#sudah jadi dictionary
        
        qry = Items.query.get(args["item_id"])
        if qry is None:
            return {'status': 'NOT_FOUND','message':'item not found'},404, { 'Content-Type': 'application/json' }
        json_item = marshal(qry,Items.respon_fields)
        nama_item = json_item["nama"]
        harga = json_item["harga"] * args["qty"]
        created_at = datetime.now()
        updated_at = datetime.now()
        
        cart_detail = Cartdetail(None,cart_id,args["item_id"],nama_item,args["qty"],harga,created_at,updated_at)
        db.session.add(cart_detail)
        db.session.commit()
        feedback = marshal(cart_detail,Cartdetail.respon_fields) 
        return feedback, 200, { 'Content-Type': 'application/json' }
    
    @jwt_required
    def delete(self,cart_id,id):
        status = get_jwt_claims()['status']
        if status != "customer" and status != "admin":
            return {'message':'Only customer and admin'},404, { 'Content-Type': 'application/json' }
        if status == "customer":
            qry = Cartdetail.query.filter_by(cart_id=cart_id).filter_by(id=id).first()
        else:
            qry = Cartdetail.query.filter_by(id=id).first()
        if qry is not None:
            db.session.delete(qry)
            db.session.commit()
            return str(marshal(qry, Cartdetail.respon_fields))+"has been deleted",200, { 'Content-Type': 'application/json' }
        return {'status': 'NOT_FOUND','message':'item not found'},404, { 'Content-Type': 'application/json' }

    def put(self):
        return 'Not yet implement', 501


api.add_resource(CartsDetailResource, '/<int:cart_id>','/<int:cart_id>/<int:id>')