# packages
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# initializa application
app = Flask(__name__)

# capture the current dir
basedir = os.path.abspath(os.path.dirname(__file__))

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'dq.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

# Initialize database
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)

# Products Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

    # constructor
    def __init__(self, name, description, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.description = description

# Product schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'quantity')

# Initialize schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


'''
Creating Routes or API end points
'''
# creating a product
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    price = request.json['price']
    quantity = request.json['quantity']
    description = request.json['description']

    # create product
    new_product = Product(name, description, price, quantity)

    #  to add the product
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

# get all products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    returned_products = products_schema.dump(all_products)
    return jsonify(returned_products)

# get single products
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    returned_product = product_schema.jsonify(product)
    return returned_product
 
# update a product
@app.route('/product/<id>', methods = ['PUT'])
def update_product(id):
    product = Product.query.get(id)

    name = request.json['name']
    price = request.json['price']
    quantity = request.json['quantity']
    description = request.json['description']

    product.name = name
    product.price = price
    product.description = description
    product.quantity = quantity

    #  to add the product
    db.session.commit()

    return product_schema.jsonify(product)

# delete product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)

# start server
if __name__ == '__main__':
    app.run(debug=True)