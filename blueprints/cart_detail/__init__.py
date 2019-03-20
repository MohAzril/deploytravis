import random, logging
from blueprints import db
from flask_restful import fields

#Items CLASS
class Cartdetail(db.Model): 
    __tablename__ = "cartdetail"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    cart_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer)
    nama_item = db.Column(db.String(200))
    qty = db.Column(db.Integer)
    harga = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    respon_fields = {
        'id': fields.Integer,
        'cart_id' : fields.Integer,
        'item_id' : fields.Integer,
        'nama_item' : fields.String,
        'qty' : fields.Integer,
        'harga' : fields.Integer,
        'created_at':fields.DateTime,
        'updated_at':fields.DateTime

    }

    def __init__(self,id,cart_id,item_id,nama_item,qty,harga,created_at,updated_at):
        self.id = id 
        self.cart_id = cart_id
        self.item_id = item_id
        self.nama_item = nama_item 
        self.qty = qty
        self.harga = harga
        self.created_at = created_at 
        self.updated_at = updated_at 

    #return repr harus string
    def __repr__(self):
        return '<Cartdetail %r>' % self.id
    