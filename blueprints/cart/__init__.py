import random, logging
from blueprints import db
from flask_restful import fields

#Items CLASS
class Cart(db.Model): 
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    customer_id = db.Column(db.Integer)
    status = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    respon_fields = {
        'id': fields.Integer,
        'customer_id' : fields.Integer,
        'status' : fields.String,
        'created_at':fields.DateTime,
        'updated_at':fields.DateTime

    }

    def __init__(self,id,customer_id,status,created_at,updated_at):
        self.id = id 
        self.customer_id = customer_id
        self.status = status
        self.created_at = created_at 
        self.updated_at = updated_at 

    #return repr harus string
    def __repr__(self):
        return '<Cart %r>' % self.id
    