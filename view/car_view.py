import json
from http import HTTPStatus

from flask import Blueprint, request, Response

from controller import CarController, AccountController
from repository import CarRepository, ReservationRepository
from model.account import AccountPrivilege
from service import ReportContext, UserReportStrategy, ManagerReportStrategy

report_context = ReportContext()
user_report_strategy = UserReportStrategy()
manager_report_strategy = ManagerReportStrategy()


def create_car_blueprint(car_controller: CarController, account_controller: AccountController,
                         car_repository: CarRepository, reservation_repository: ReservationRepository):
    car_blueprint = Blueprint("car_blueprint", __name__)

    @car_blueprint.route("/api/cars", methods=["GET"])
    def get_all_cars():
        result = car_controller.get_all_entities()
        if result["status"] == 404:
            return Response(response=result["response"], status=HTTPStatus(result["status"]))
        return Response(response=json.dumps([entity.to_dict() for entity in result["response"]]),
                        status=HTTPStatus(result["status"]))

    @car_blueprint.route("/api/cars/<int:car_id>", methods=["GET"])
    def get_car_by_id(car_id):
        result = car_controller.get_entity_by_id(entity_id=car_id)
        if result["status"] == 404:
            return Response(response=result["response"], status=HTTPStatus(result["status"]))
        return Response(response=json.dumps(result["response"].to_dict()),
                        status=HTTPStatus(result["status"]))

    @car_blueprint.route('/api/cars/image/<int:car_id>', methods=['GET'])
    def get_car_image_by_id(car_id):
        result = car_controller.get_entity_image_by_id(entity_id=car_id)
        return Response(response=result["response"], status=HTTPStatus(result["status"]))

    @car_blueprint.route('/api/cars/add', methods=['POST'])
    def add_car():
        car_data = request.json
        result = car_controller.add_entity(**car_data)
        return Response(response=result["response"], status=HTTPStatus(result["status"]))

    @car_blueprint.route("/api/cars/update/<int:car_id>", methods=["PUT"])
    def update_car(car_id):
        car_data = request.json
        result = car_controller.update_entity(entity_id=car_id, **car_data)
        return Response(response=result["response"], status=HTTPStatus(result["status"]))

    @car_blueprint.route("/api/cars/delete/<int:car_id>", methods=["DELETE"])
    def delete_car(car_id):
        result = car_controller.delete_entity(entity_id=car_id)
        return Response(response=result["response"], status=HTTPStatus(result["status"]))

    @car_blueprint.route('/api/cars/report', methods=['GET'])
    def get_cars_report():
        account_creds = request.json
        if 'email' not in account_creds or 'password' not in account_creds:
            return Response(status=HTTPStatus.BAD_REQUEST, response="Incorrect request body.")
        result = account_controller.check_entity(email=account_creds['email'],
                                                 password=account_creds['password'])
        if result["status"] == 200:
            account = result["response"]
            if account.privilege_level == AccountPrivilege.COMMON:
                report_context.set_strategy(user_report_strategy)
            elif account.privilege_level == AccountPrivilege.PRIVILEDGED:
                report_context.set_strategy(manager_report_strategy)
            else:
                return Response(response="No such privilege level.", status=HTTPStatus(404))
            data = report_context.create_report(
                car_repository=car_repository,
                reservation_repository=reservation_repository,
            )
            return Response(response=json.dumps(data), status=HTTPStatus(200))
        else:
            return Response(response=result["response"], status=HTTPStatus(result["status"]))

    @car_blueprint.route('/api/cars/filtered', methods=['GET'])
    def get_filtered_cars():
        filters = request.args.to_dict()
        result = car_controller.get_filtered_entities(**filters)
        return Response(response=json.dumps([entity.to_dict() for entity in result["response"]]),
                        status=HTTPStatus(result["status"]))

    return car_blueprint
