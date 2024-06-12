# app/routes/reservations.py
from flask import Blueprint, request, jsonify
from app import db
from app.models import Reservation

bp = Blueprint('reservations', __name__, url_prefix='/reservations')

@bp.route('', methods=['GET'])
def list_reservations():
    reservations = Reservation.query.all()
    return jsonify([r.serialize() for r in reservations])

@bp.route('/<int:id>', methods=['GET'])
def get_reservation(id):
    reservation = Reservation.query.get_or_404(id)
    return jsonify(reservation.serialize())

@bp.route('', methods=['POST'])
def create_reservation():
    data = request.get_json()
    new_reservation = Reservation(**data)
    db.session.add(new_reservation)
    db.session.commit()
    return jsonify(new_reservation.serialize()), 201

@bp.route('/<int:id>', methods=['PUT'])
def update_reservation(id):
    reservation = Reservation.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(reservation, key, value)
    db.session.commit()
    return jsonify(reservation.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete_reservation(id):
    reservation = Reservation.query.get_or_404(id)
    db.session.delete(reservation)
    db.session.commit()
    return '', 204
