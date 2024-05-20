import datetime
from flask import Blueprint, request

from model import db_service
from repository import ReservationRepository
from controller import ReservationController

reservation_repository = ReservationRepository(db_manager=db_service)
reservation_controller = ReservationController(reservation_repository)

reservation_blueprint = Blueprint('reservation_blueprint', __name__)


@reservation_blueprint.route('/reservations', methods=['GET'])
def get_all_reservations():
    return reservation_controller.get_all_entities()


@reservation_blueprint.route('/reservations/<int:reservation_id>', methods=['GET'])
def get_reservation_by_id(reservation_id):
    return reservation_controller.get_entity_by_id(entity_id=reservation_id)


@reservation_blueprint.route('/api/reservations/add', methods=['POST'])
def add_reservation():
    reservation_data = request.json
    reservation_data['start_date'] = datetime.date.fromisoformat(reservation_data['start_date'])
    reservation_data['end_date'] = datetime.date.fromisoformat(reservation_data['end_date'])
    reservation_data['expected_profit'] = (reservation_data['end_date'] - reservation_data['start_date']).days * 30
    reservation_data['money_status'] = reservation_data['expected_profit'] + 300
    return reservation_controller.add_entity(**reservation_data)


@reservation_blueprint.route('/reservations/update/<int:reservation_id>', methods=['PUT'])
def update_reservation(reservation_id):
    reservation_data = request.json
    return reservation_controller.update_entity(entity_id=reservation_id, **reservation_data)


@reservation_blueprint.route('/reservations/delete/<int:reservation_id>', methods=['DELETE'])
def delete_reservation(reservation_id):
    return reservation_controller.delete_entity(entity_id=reservation_id)
