import logging, json
from flask import Blueprint, Flask, request
from flask_restful import Api, Resource, reqparse, marshal
from time import strftime 
from logging.handlers import RotatingFileHandler
from flask_jwt_extended import jwt_required, get_jwt_claims
import random
#add __init__.py
from . import *
from blueprints.users import *
from blueprints import db
from datetime import date, datetime

bp_cart = Blueprint('cart', __name__)
api = Api(bp_cart)

class CartsResource(Resource):

    def __init__(self):
        pass
    
    @jwt_required
    def get(self,id=None):
        status = get_jwt_claims()['status']
        if status != "customer" and status != "admin":
            return {'message':'Only customer and admin'},404, { 'Content-Type': 'application/json' }
        if id is None:
            parser = reqparse.RequestParser()
            parser.add_argument('p',type=int, location='args', default=1)
            parser.add_argument('rp',type=int, location='args', default=5)
            parser.add_argument('id',type=int, location='args')
            parser.add_argument('status', location='args')
            args = parser.parse_args()#sudah jadi dictionary    
            
            offset = (args['p'] * args['rp']) - args['rp']
            
            customer_id = get_jwt_claims()['user_id']
            if status == "customer":
                qry = Cart.query.filter_by(customer_id=customer_id)
            else:
                qry = Cart.query

            if args['status'] is not None:
                qry = qry.filter_by(status=args['status'])

            if args['id'] is not None:
                qry = qry.filter_by(id=args['id'])

            rows = [{'page':args['p']}]
            for row in qry.limit(args['rp']).offset(offset).all():
                temp = marshal(row, Cart.respon_fields)
                rows.append(temp)

            return rows, 200, { 'Content-Type': 'application/json' }
        else :
            customer_id = get_jwt_claims()['user_id']
            if status == "customer":
                qry = Cart.query.filter_by(customer_id=customer_id).filter_by(id=id).first()
            else:
                qry = Cart.query.filter_by(id=id).first()
            if qry is not None:
                temp = marshal(qry, Cart.respon_fields)
                return temp, 200, { 'Content-Type': 'application/json' }
            return {'status': 'NOT_FOUND','message':'item not found'},404, { 'Content-Type': 'application/json' }
    
    @jwt_required
    def post(self):
        status = get_jwt_claims()['status']
        if status != "customer":
            return {'message':'Only customer can post cart'},404, { 'Content-Type': 'application/json' }

        customer_id = get_jwt_claims()['user_id']
        status = "not yet paid"
        created_at = datetime.now()
        updated_at = datetime.now()

        cart = Cart(None,customer_id,status,created_at,updated_at)
        db.session.add(cart)
        db.session.commit()
        feedback = marshal(cart,Cart.respon_fields) 
        return feedback, 200, { 'Content-Type': 'application/json' }
    
    @jwt_required
    def delete(self,id):
        status = get_jwt_claims()['status']
        if status != "customer" and status != "admin":
            return {'message':'Only customer and admin'},404, { 'Content-Type': 'application/json' }
        customer_id = get_jwt_claims()['user_id']
        if status == "customer":
            qry = Cart.query.filter_by(customer_id=customer_id).filter_by(id=id).first()
        else:
            qry = Cart.query.filter_by(id=id).first()
        if qry is not None:
            db.session.delete(qry)
            db.session.commit()
            return str(marshal(qry, Cart.respon_fields))+"has been deleted",200, { 'Content-Type': 'application/json' }
        return {'status': 'NOT_FOUND','message':'item not found'},404, { 'Content-Type': 'application/json' }

    def put(self):
        return 'Not yet implement', 501


api.add_resource(CartsResource, '','/<int:id>')