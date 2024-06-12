from flask import Blueprint, request, jsonify
from app import db
from app.models import Restaurant
from app.decorators import role_required

bp = Blueprint('restaurants', __name__, url_prefix='/restaurants')

@bp.route('', methods=['GET'])
def list_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([r.serialize() for r in restaurants])

@bp.route('/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    return jsonify(restaurant.serialize())

@bp.route('', methods=['POST'])
@role_required('admin')
def create_restaurant():
    data = request.get_json()
    new_restaurant = Restaurant(**data)
    db.session.add(new_restaurant)
    db.session.commit()
    return jsonify(new_restaurant.serialize()), 201

@bp.route('/<int:id>', methods=['PUT'])
@role_required('admin')
def update_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(restaurant, key, value)
    db.session.commit()
    return jsonify(restaurant.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
@role_required('admin')
def delete_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    db.session.delete(restaurant)
    db.session.commit()
    return '', 204
