from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os
import logging
import json

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Product Class/Model
class users(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)
  mail = db.Column(db.String(200))
  Number = db.Colum(db.Integer)

  def __init__(id, name, mail, Numer):
    self.name = name
    self.mail = mail
    self.Number = Numer

# Product Schema
class usersSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'mail', 'Number')

# Init schema
users_schema = usersSchema()
users_schema = usersSchema(many=True)

# Create a Product
@app.route('/users', methods=['POST'])
def add_product():
  app.logger.info("Request body" + request.json["name"])
  name = request.json['name']
  mail = request.json['mail']
  Number = request.json['Number']
  

  new_users = users(name, mail, Number)

  db.session.add(new_users)
  db.session.commit()

  return users_schema.jsonify(new_users)

# Get All Products
@app.route('/users', methods=['GET'])
def get_products():
  all_products = users.query.all()
  result = users_schema.dump(all_products)
  return jsonify(result)

# Get Single Products
@app.route('/users/<id>', methods=['GET'])
def get_product(id):
  product = users.query.get(id)
  return users_schema.jsonify(product)

# Update a Product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
  product = users.query.get(id)

  name = request.json['name']
  mail = request.json['mail']
  Number = request.json['Number']
  

  users.name = name
  users.mail = mail
  users.Number = Number
  

  db.session.commit()

  return users_schema.jsonify(product)

# Delete Product
@app.route('/users/<id>', methods=['DELETE'])
def delete_product(id):
  product = users.query.get(id)
  db.session.delete(product)
  db.session.commit()

  return users_schema.jsonify(product)

# Run Server
if __name__ == '__main__':
  app.run(debug=True)