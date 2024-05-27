import datetime
import json
from http import HTTPStatus

from flask import Blueprint, request, Response

from controller import ReservationController, AccountController
from model.reservation import ReservationStatus


def create_reservation_blueprint(reservation_controller: ReservationController, account_controller: AccountController):
    reservation_blueprint = Blueprint('reservation_blueprint', __name__)

    @reservation_blueprint.route('/api/reservations', methods=['GET'])
    def get_all_reservations():
        result = reservation_controller.get_all_entities()
        if result["status"] == 404:
            return Response(response=result["response"], status=HTTPStatus(result["status"]))
        return Response(response=json.dumps([entity.to_dict() for entity in result["response"]]),
                        status=HTTPStatus(result["status"]))

    @reservation_blueprint.route('/api/reservations/<int:reservation_id>', methods=['GET'])
    def get_reservation_by_id(reservation_id):
        result = reservation_controller.get_entity_by_id(entity_id=reservation_id)
        if result["status"] == 404:
            return Response(response=result["response"], status=HTTPStatus(result["status"]))
        return Response(response=json.dumps(result["response"].to_dict()),
                        status=HTTPStatus(result["status"]))

    @reservation_blueprint.route('/api/reservations/add', methods=['POST'])
    def add_reservation():
        reservation_data = request.json
        reservation_data['start_date'] = datetime.datetime.fromisoformat(reservation_data['start_date'])
        reservation_data['end_date'] = datetime.datetime.fromisoformat(reservation_data['end_date'])
        reservation_data['expected_profit'] = (reservation_data['end_date'] - reservation_data['start_date']).days * 30
        reservation_data['money_status'] = reservation_data['expected_profit'] + 300
        result = reservation_controller.get_ongoing_reservations_by_car_id(reservation_data["car_id"])
        if result is not None:
            ongoing_reservations = result["response"]
            for ongoing_reservation in ongoing_reservations:
                if ((ongoing_reservation.end_date >= reservation_data["end_date"] >= ongoing_reservation.start_date) or
                        (ongoing_reservation.end_date >= reservation_data[
                            "start_date"] >= ongoing_reservation.start_date) or
                        (ongoing_reservation.end_date <= reservation_data[
                            "end_date"] and ongoing_reservation.start_date >= reservation_data["start_date"])):
                    return Response(response="Already reserved for these dates.", status=HTTPStatus(409))
        result = reservation_controller.add_entity(**reservation_data)
        return Response(response=result["response"], status=HTTPStatus(result["status"]))

    @reservation_blueprint.route('/api/reservations/users/<int:account_id>', methods=['GET'])
    def get_all_reservations_by_user(account_id):
        account_creds = request.headers
        if 'X-email' not in account_creds or 'X-password' not in account_creds:
            return Response(status=HTTPStatus.BAD_REQUEST, response="You must provide email and password for login")
        account_check = account_controller.check_entity(email=account_creds['X-email'],
                                                        password=account_creds['X-password'])
        if account_check["status"] == HTTPStatus.OK:
            result = reservation_controller.get_all_entities_by_account_id(account_id)
            return Response(response=json.dumps([entity.to_dict() for entity in result["response"]]),
                            status=HTTPStatus(result["status"]))
        else:
            return Response(response=account_check["response"], status=HTTPStatus(account_check["status"]))

    @reservation_blueprint.route('/api/reservations/update/<int:reservation_id>', methods=['PUT'])
    def update_reservation(reservation_id):
        reservation_data = request.json
        result = reservation_controller.update_entity(entity_id=reservation_id, **reservation_data)
        return Response(response=result["response"], status=HTTPStatus(result["status"]))

    @reservation_blueprint.route('/api/reservations/<int:reservation_id>/cancel', methods=['PUT'])
    def cancel_reservation(reservation_id):
        result = reservation_controller.update_entity(entity_id=reservation_id, status=ReservationStatus.CANCELED)
        return Response(response=result["response"], status=HTTPStatus(result["status"]))

    @reservation_blueprint.route('/api/reservations/<int:reservation_id>/confirm', methods=['PUT'])
    def confirm_reservation(reservation_id):
        result = reservation_controller.update_entity(entity_id=reservation_id, status=ReservationStatus.CONFIRMED)
        return Response(response=result["response"], status=HTTPStatus(result["status"]))

    @reservation_blueprint.route('/api/reservations/<int:reservation_id>/confirm-take', methods=['PUT'])
    def confirm_take_reservation(reservation_id):
        result = reservation_controller.update_entity(entity_id=reservation_id, status=ReservationStatus.IS_USED)
        return Response(response=result["response"], status=HTTPStatus(result["status"]))

    @reservation_blueprint.route('/api/reservations/<int:reservation_id>/confirm-return', methods=['PUT'])
    def confirm_ret_reservation(reservation_id):
        result = reservation_controller.update_entity(entity_id=reservation_id, status=ReservationStatus.WAITING_CHECK)
        return Response(response=result["response"], status=HTTPStatus(result["status"]))

    @reservation_blueprint.route('/api/reservations/<int:reservation_id>/confirm-check', methods=['PUT'])
    def check_reservation(reservation_id):
        reservation_data = request.json
        result = reservation_controller.update_entity(entity_id=reservation_id,
                                                      status=ReservationStatus.WAITING_PAYMENT,
                                                      fines=reservation_data['fines'])
        return Response(response=result["response"], status=HTTPStatus(result["status"]))

    @reservation_blueprint.route('/api/reservations/<int:reservation_id>/final-payment', methods=['PUT'])
    def final_pay_reservation(reservation_id):
        result = reservation_controller.update_entity(entity_id=reservation_id, status=ReservationStatus.COMPLETED)
        return Response(response=result["response"], status=HTTPStatus(result["status"]))

    @reservation_blueprint.route('/api/reservations/delete/<int:reservation_id>', methods=['DELETE'])
    def delete_reservation(reservation_id):
        result = reservation_controller.delete_entity(entity_id=reservation_id)
        return Response(response=result["response"], status=HTTPStatus(result["status"]))

    @reservation_blueprint.route('/api/reservations/cars/<int:car_id>', methods=['GET'])
    def get_all_reservations_by_car(car_id):
        result = reservation_controller.get_ongoing_reservations_by_car_id(car_id)
        return Response(response=json.dumps([entity.to_dict() for entity in result["response"]]),
                        status=HTTPStatus(result["status"]))

    return reservation_blueprint
