#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    
    bakery_array = []
    for bakery in Bakery.query.all():
        bakery_dict = bakery.to_dict()
        # bakery_dict = {
        #     "name": bakery.name,
        #     "id": bakery.id,
        # }

        bakery_array.append(bakery_dict)

    response = make_response(
        jsonify(bakery_array),
        200,
        {"Content-Type": "application/json"}
    )

    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()

    if not bakery:
        response_body = '<h1>404 Bakery not found</h1>'
        response = make_response(response_body, 404)
        return response
    
    bakery_dict = bakery.to_dict()

    response = make_response(
        jsonify(bakery_dict),
        200,
        {"Content-Type": "application/json"}
    )

    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    bg_array = []
    for baked_good in BakedGood.query.order_by(BakedGood.price.asc()).all():
        bg_dict = baked_good.to_dict()
        bg_array.append(bg_dict)

    response = make_response(
        jsonify(bg_array),
        200,
        {"Content-Type": "application/json"}
    )

    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    bg_dict = baked_good.to_dict()

    response = make_response(
        jsonify(bg_dict),
        200,
        {"Content-Type": "application/json"}
    )

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
